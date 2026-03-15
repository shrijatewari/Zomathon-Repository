"""
Simulation Engine - Generates real-time dispatch events.
"""

import numpy as np
import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import random


@dataclass
class DispatchEvent:
    """Represents a dispatch event."""
    event_type: str  # ORDER_CREATED, KPT_PREDICTED, RIDER_DISPATCHED, etc.
    order_id: str
    timestamp: str
    data: Dict


class SimulationEngine:
    """
    Generates realistic dispatch events for real-time simulation.
    """
    
    def __init__(self, arrival_rate: float = 0.5):
        """
        Initialize simulation engine.
        
        Parameters:
        -----------
        arrival_rate : float
            Orders per minute (Poisson rate)
        """
        self.arrival_rate = arrival_rate
        self.order_counter = 0
        self.active_orders: Dict[str, Dict] = {}
        self.riders = [
            {'id': f'RIDER_{i}', 'available': True, 'lat': 0.0, 'lon': 0.0}
            for i in range(10)
        ]
        self.restaurants = [
            {'id': f'REST_{i}', 'lat': np.random.uniform(-1, 1), 'lon': np.random.uniform(-1, 1)}
            for i in range(5)
        ]
    
    def generate_order_created(self) -> DispatchEvent:
        """Generate ORDER_CREATED event."""
        self.order_counter += 1
        order_id = f"ORD_{self.order_counter:06d}"
        
        restaurant = random.choice(self.restaurants)
        
        self.active_orders[order_id] = {
            'order_id': order_id,
            'restaurant_id': restaurant['id'],
            'created_at': datetime.now(),
            'status': 'created'
        }
        
        return DispatchEvent(
            event_type="ORDER_CREATED",
            order_id=order_id,
            timestamp=datetime.now().isoformat(),
            data={
                'restaurant_id': restaurant['id'],
                'restaurant_lat': restaurant['lat'],
                'restaurant_lon': restaurant['lon']
            }
        )
    
    def generate_kpt_predicted(
        self,
        order_id: str,
        predicted_kpt: float,
        confidence: float
    ) -> DispatchEvent:
        """Generate KPT_PREDICTED event."""
        return DispatchEvent(
            event_type="KPT_PREDICTED",
            order_id=order_id,
            timestamp=datetime.now().isoformat(),
            data={
                'predicted_kpt': predicted_kpt,
                'confidence': confidence,
                'lower_bound': predicted_kpt - 1.96 * confidence,
                'upper_bound': predicted_kpt + 1.96 * confidence
            }
        )
    
    def generate_rider_dispatched(
        self,
        order_id: str,
        rider_id: str,
        dispatch_time: float,
        travel_time: float
    ) -> DispatchEvent:
        """Generate RIDER_DISPATCHED event."""
        if order_id in self.active_orders:
            self.active_orders[order_id]['rider_id'] = rider_id
            self.active_orders[order_id]['status'] = 'dispatched'
            self.active_orders[order_id]['dispatch_time'] = dispatch_time
        
        # Mark rider as unavailable
        for rider in self.riders:
            if rider['id'] == rider_id:
                rider['available'] = False
                break
        
        return DispatchEvent(
            event_type="RIDER_DISPATCHED",
            order_id=order_id,
            timestamp=datetime.now().isoformat(),
            data={
                'rider_id': rider_id,
                'dispatch_time': dispatch_time,
                'travel_time': travel_time,
                'estimated_arrival': dispatch_time + travel_time
            }
        )
    
    def generate_rider_moved(
        self,
        order_id: str,
        rider_id: str,
        progress: float
    ) -> DispatchEvent:
        """Generate RIDER_MOVED event (rider traveling to restaurant)."""
        if order_id in self.active_orders:
            order = self.active_orders[order_id]
            restaurant = next(
                r for r in self.restaurants if r['id'] == order['restaurant_id']
            )
            
            # Simulate rider position
            rider = next(r for r in self.riders if r['id'] == rider_id)
            rider['lat'] = restaurant['lat'] * progress
            rider['lon'] = restaurant['lon'] * progress
        
        return DispatchEvent(
            event_type="RIDER_MOVED",
            order_id=order_id,
            timestamp=datetime.now().isoformat(),
            data={
                'rider_id': rider_id,
                'progress': progress,
                'rider_lat': rider['lat'],
                'rider_lon': rider['lon']
            }
        )
    
    def generate_rider_arrived(
        self,
        order_id: str,
        rider_id: str
    ) -> DispatchEvent:
        """Generate RIDER_ARRIVED event."""
        if order_id in self.active_orders:
            self.active_orders[order_id]['status'] = 'rider_arrived'
        
        return DispatchEvent(
            event_type="RIDER_ARRIVED",
            order_id=order_id,
            timestamp=datetime.now().isoformat(),
            data={
                'rider_id': rider_id
            }
        )
    
    def generate_order_picked_up(
        self,
        order_id: str,
        rider_id: str
    ) -> DispatchEvent:
        """Generate ORDER_PICKED_UP event."""
        if order_id in self.active_orders:
            self.active_orders[order_id]['status'] = 'picked_up'
            del self.active_orders[order_id]
        
        # Mark rider as available
        for rider in self.riders:
            if rider['id'] == rider_id:
                rider['available'] = True
                break
        
        return DispatchEvent(
            event_type="ORDER_PICKED_UP",
            order_id=order_id,
            timestamp=datetime.now().isoformat(),
            data={
                'rider_id': rider_id
            }
        )
    
    def generate_kitchen_started(self, order_id: str) -> DispatchEvent:
        """Generate KITCHEN_STARTED event (kitchen begins preparing order)."""
        return DispatchEvent(
            event_type="KITCHEN_STARTED",
            order_id=order_id,
            timestamp=datetime.now().isoformat(),
            data={
                'status': 'preparing',
                'estimated_completion': None
            }
        )
    
    def generate_food_preparing(self, order_id: str, progress: float) -> DispatchEvent:
        """Generate FOOD_PREPARING event (kitchen preparation progress)."""
        return DispatchEvent(
            event_type="FOOD_PREPARING",
            order_id=order_id,
            timestamp=datetime.now().isoformat(),
            data={
                'progress': progress,
                'status': 'cooking'
            }
        )
    
    def generate_food_ready(self, order_id: str) -> DispatchEvent:
        """Generate FOOD_READY event (kitchen finished preparing)."""
        return DispatchEvent(
            event_type="FOOD_READY",
            order_id=order_id,
            timestamp=datetime.now().isoformat(),
            data={
                'status': 'ready_for_pickup'
            }
        )
    
    def generate_rider_en_route(self, order_id: str, rider_id: str, progress: float) -> DispatchEvent:
        """Generate RIDER_EN_ROUTE event (rider delivering to customer)."""
        return DispatchEvent(
            event_type="RIDER_EN_ROUTE",
            order_id=order_id,
            timestamp=datetime.now().isoformat(),
            data={
                'rider_id': rider_id,
                'progress': progress,
                'status': 'delivering'
            }
        )
    
    def generate_order_delivered(self, order_id: str, rider_id: str) -> DispatchEvent:
        """Generate ORDER_DELIVERED event (order completed)."""
        # Mark rider as available
        for rider in self.riders:
            if rider['id'] == rider_id:
                rider['available'] = True
                break
        
        return DispatchEvent(
            event_type="ORDER_DELIVERED",
            order_id=order_id,
            timestamp=datetime.now().isoformat(),
            data={
                'rider_id': rider_id,
                'status': 'completed'
            }
        )
    
    def get_available_rider(self) -> Optional[str]:
        """Get an available rider ID."""
        available = [r for r in self.riders if r['available']]
        if available:
            return random.choice(available)['id']
        return None
    
    def estimate_travel_time(self, restaurant_id: str) -> float:
        """Estimate travel time to restaurant (simulated)."""
        # Simulate travel time between 3-8 minutes
        return np.random.uniform(3.0, 8.0)


if __name__ == "__main__":
    # Test simulation engine
    engine = SimulationEngine()
    
    event = engine.generate_order_created()
    print(f"Event: {event.event_type}")
    print(f"Order: {event.order_id}")
    print(f"Data: {event.data}")
