"""
FastAPI WebSocket Server for Real-Time Dispatch Events.

Provides WebSocket endpoint /ws/dispatch that streams dispatch decisions.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import numpy as np
from typing import List
from datetime import datetime

from dispatch_engine import DispatchEngine
from prediction_service import PredictionService
from reconstruction_service import ReconstructionService
from signal_filter import DEFAULT_RELIABILITY_SCORES
from simulation_engine import SimulationEngine, DispatchEvent
from telemetry_service import TelemetryService

app = FastAPI(title="PrepSense Dispatch Engine")

# CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
dispatch_engine = DispatchEngine(cost_idle=1.0, cost_delay=2.0)
prediction_service = PredictionService()
simulation_engine = SimulationEngine(arrival_rate=0.5)
telemetry_service = TelemetryService()
reconstruction_service = ReconstructionService()

# Active WebSocket connections
active_connections: List[WebSocket] = []


async def broadcast_message(message: dict):
    """Broadcast message to all connected clients."""
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            print(f"Error sending message: {e}")
            disconnected.append(connection)
    
    # Remove disconnected clients
    for conn in disconnected:
        if conn in active_connections:
            active_connections.remove(conn)


async def emit_filtered_update(
    order_id: str,
    signal_type: str,
    state: dict,
    base_value: float,
):
    """
    Generate a noisy telemetry observation and push the filtered estimate.
    """
    observation = telemetry_service.build_observation(
        order_id=order_id,
        signal_type=signal_type,
        true_packed_time=state["true_packed_time"],
        queue_length=state.get("queue_length", 0.0),
        base_value=base_value,
    )
    filtered_update = reconstruction_service.update_estimate(
        order_id=order_id,
        signal_type=signal_type,
        observed_signal=observation["observed_signal"],
        reliability_score=observation["reliability_score"],
        queue_length=observation["queue_length"],
        timestamp=observation["timestamp"],
        true_packed_time=state["true_packed_time"],
    )
    await broadcast_message(
        {
            "event_type": "FILTERED_SIGNAL_UPDATED",
            **filtered_update,
        }
    )


async def simulate_dispatch_events():
    """
    Simulate real-time dispatch events and broadcast via WebSocket.
    
    Generates events every 200ms as specified.
    """
    order_states = {}  # Track order lifecycle
    
    while True:
        try:
            # Generate new order with Poisson process - INCREASED RATE
            if np.random.random() < 0.3:  # Increased from 0.1 to 0.3 for more events (~1.5 orders/min)
                event = simulation_engine.generate_order_created()
                order_id = event.order_id
                queue_length = float(np.random.randint(0, 6))
                true_packed_time = float(np.random.uniform(8.0, 18.0) + queue_length * 0.8)
                order_states[order_id] = {
                    'created': True,
                    'predicted': False,
                    'dispatched': False,
                    'arrived': False,
                    'picked_up': False,
                    'restaurant_id': event.data.get('restaurant_id', 'REST_0'),
                    'queue_length': queue_length,
                    'true_packed_time': true_packed_time,
                }
                
                await broadcast_message({
                    'event_type': event.event_type,
                    'order_id': order_id,
                    'timestamp': event.timestamp,
                    **event.data
                })
                await emit_filtered_update(
                    order_id=order_id,
                    signal_type="kitchen_queue_snapshot",
                    state=order_states[order_id],
                    base_value=true_packed_time + queue_length * 0.35,
                )
            
            # Process active orders
            for order_id, state in list(order_states.items()):
                # Predict KPT if not done
                if not state['predicted']:
                    queue_length = int(state.get('queue_length', np.random.randint(0, 5)))
                    orders_last_10min = np.random.randint(0, 10)
                    
                    predicted_kpt, confidence = prediction_service.predict_kpt(
                        queue_length=queue_length,
                        orders_last_10min=orders_last_10min
                    )
                    
                    event = simulation_engine.generate_kpt_predicted(
                        order_id, predicted_kpt, confidence
                    )
                    
                    state['predicted'] = True
                    state['predicted_kpt'] = predicted_kpt
                    state['confidence'] = confidence
                    
                    await broadcast_message({
                        'event_type': event.event_type,
                        'order_id': order_id,
                        'timestamp': event.timestamp,
                        **event.data
                    })
                    await emit_filtered_update(
                        order_id=order_id,
                        signal_type="merchant_ready_time",
                        state=state,
                        base_value=state["true_packed_time"] + np.random.normal(1.8, 1.2),
                    )
                    
                    # Kitchen starts preparing
                    kitchen_event = simulation_engine.generate_kitchen_started(order_id)
                    await broadcast_message({
                        'event_type': kitchen_event.event_type,
                        'order_id': order_id,
                        'timestamp': kitchen_event.timestamp,
                        **kitchen_event.data
                    })
                    
                    # Make dispatch decision
                    rider_id = simulation_engine.get_available_rider()
                    if rider_id:
                        restaurant_id = order_states[order_id].get('restaurant_id', 'REST_0')
                        travel_time = simulation_engine.estimate_travel_time(restaurant_id)
                        
                        decision = dispatch_engine.make_dispatch_decision(
                            order_id=order_id,
                            predicted_kpt=predicted_kpt,
                            confidence=confidence,
                            travel_time=travel_time
                        )
                        
                        event = simulation_engine.generate_rider_dispatched(
                            order_id, rider_id, decision.dispatch_time, travel_time
                        )
                        
                        state['dispatched'] = True
                        state['rider_id'] = rider_id
                        state['dispatch_time'] = decision.dispatch_time
                        state['kitchen_progress'] = 0.0
                        
                        await broadcast_message({
                            'event_type': event.event_type,
                            'order_id': order_id,
                            'timestamp': event.timestamp,
                            **event.data,
                            'predicted_kpt': predicted_kpt,
                            'confidence': confidence,
                            'dispatch_time': decision.dispatch_time,
                            'idle_risk': decision.idle_risk,
                            'delay_risk': decision.delay_risk
                        })
                
                # Simulate kitchen preparation progress
                elif state['dispatched'] and not state.get('food_ready', False):
                    kitchen_progress = min(1.0, state.get('kitchen_progress', 0) + 0.15)
                    state['kitchen_progress'] = kitchen_progress
                    
                    if kitchen_progress < 1.0:
                        # Send food preparing progress
                        food_event = simulation_engine.generate_food_preparing(
                            order_id, kitchen_progress
                        )
                        await broadcast_message({
                            'event_type': food_event.event_type,
                            'order_id': order_id,
                            'timestamp': food_event.timestamp,
                            **food_event.data
                        })
                        await emit_filtered_update(
                            order_id=order_id,
                            signal_type="kitchen_queue_snapshot",
                            state=state,
                            base_value=state["true_packed_time"] + (1.0 - kitchen_progress) * 1.2,
                        )
                    else:
                        # Food is ready
                        food_ready_event = simulation_engine.generate_food_ready(order_id)
                        state['food_ready'] = True
                        await broadcast_message({
                            'event_type': food_ready_event.event_type,
                            'order_id': order_id,
                            'timestamp': food_ready_event.timestamp,
                            **food_ready_event.data
                        })
                        await emit_filtered_update(
                            order_id=order_id,
                            signal_type="merchant_ready_time",
                            state=state,
                            base_value=state["true_packed_time"],
                        )
                
                # Simulate rider movement to restaurant
                elif state['dispatched'] and state.get('food_ready', False) and not state['arrived']:
                    progress = min(1.0, state.get('progress', 0) + 0.1)
                    state['progress'] = progress
                    
                    if progress >= 1.0:
                        event = simulation_engine.generate_rider_arrived(
                            order_id, state['rider_id']
                        )
                        state['arrived'] = True
                        
                        await broadcast_message({
                            'event_type': event.event_type,
                            'order_id': order_id,
                            'timestamp': event.timestamp,
                            **event.data
                        })
                        await emit_filtered_update(
                            order_id=order_id,
                            signal_type="rider_arrival_time",
                            state=state,
                            base_value=state["true_packed_time"] + np.random.normal(0.8, 0.9),
                        )
                    else:
                        event = simulation_engine.generate_rider_moved(
                            order_id, state['rider_id'], progress
                        )
                        
                        await broadcast_message({
                            'event_type': event.event_type,
                            'order_id': order_id,
                            'timestamp': event.timestamp,
                            **event.data
                        })
                
                # Order picked up - rider starts delivery
                elif state['arrived'] and not state['picked_up']:
                    if np.random.random() < 0.3:  # 30% chance to pick up
                        event = simulation_engine.generate_order_picked_up(
                            order_id, state['rider_id']
                        )
                        state['picked_up'] = True
                        state['delivery_progress'] = 0.0
                        
                        await broadcast_message({
                            'event_type': event.event_type,
                            'order_id': order_id,
                            'timestamp': event.timestamp,
                            **event.data
                        })
                        await emit_filtered_update(
                            order_id=order_id,
                            signal_type="pickup_time",
                            state=state,
                            base_value=state["true_packed_time"] + np.random.normal(0.2, 0.35),
                        )
                
                # Rider en route to customer
                elif state['picked_up'] and not state.get('delivered', False):
                    delivery_progress = min(1.0, state.get('delivery_progress', 0) + 0.12)
                    state['delivery_progress'] = delivery_progress
                    
                    if delivery_progress < 1.0:
                        en_route_event = simulation_engine.generate_rider_en_route(
                            order_id, state['rider_id'], delivery_progress
                        )
                        await broadcast_message({
                            'event_type': en_route_event.event_type,
                            'order_id': order_id,
                            'timestamp': en_route_event.timestamp,
                            **en_route_event.data
                        })
                    else:
                        # Order delivered
                        delivered_event = simulation_engine.generate_order_delivered(
                            order_id, state['rider_id']
                        )
                        state['delivered'] = True
                        
                        await broadcast_message({
                            'event_type': delivered_event.event_type,
                            'order_id': order_id,
                            'timestamp': delivered_event.timestamp,
                            **delivered_event.data
                        })
                        
                        # Remove completed order
                        reconstruction_service.clear_order(order_id)
                        del order_states[order_id]
            
            # Wait 200ms before next update
            await asyncio.sleep(0.2)
            
        except Exception as e:
            print(f"Error in simulation loop: {e}")
            await asyncio.sleep(0.2)


@app.websocket("/ws/dispatch")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time dispatch events.
    
    Clients connect to receive dispatch decisions and updates.
    """
    await websocket.accept()
    active_connections.append(websocket)
    
    print(f"Client connected. Total connections: {len(active_connections)}")
    
    try:
        # Send welcome message
        await websocket.send_json({
            'event_type': 'CONNECTED',
            'message': 'Connected to PrepSense Dispatch Engine',
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for any incoming message (ping/pong)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                # Echo back or handle command
                if data == "ping":
                    await websocket.send_json({"type": "pong"})
            except asyncio.TimeoutError:
                # No message received, continue
                pass
            except WebSocketDisconnect:
                break
                
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)
        print(f"Client removed. Total connections: {len(active_connections)}")


@app.on_event("startup")
async def startup_event():
    """Start simulation loop when server starts."""
    print("Starting PrepSense Dispatch Engine...")
    asyncio.create_task(simulate_dispatch_events())
    print("Simulation loop started. WebSocket available at ws://localhost:8000/ws/dispatch")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "PrepSense Dispatch Engine",
        "status": "running",
        "websocket_endpoint": "/ws/dispatch",
        "connections": len(active_connections)
    }


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    import numpy as np
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
