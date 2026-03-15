# PrepSense Real-Time Dispatch Decision Engine

A production-grade real-time dispatch optimization system that converts KPT predictions into optimal rider assignment decisions.

## Architecture

- **FastAPI Backend**: WebSocket server streaming dispatch events
- **WebSocket Event Stream**: Real-time updates every 200ms
- **Streamlit Frontend**: Interactive dashboard with live visualizations

## Project Structure

```
prepsense/
├── backend/
│   ├── dispatch_engine.py      # Core dispatch optimization logic
│   ├── prediction_service.py  # KPT prediction service
│   ├── simulation_engine.py   # Event simulation
│   └── websocket_server.py    # FastAPI WebSocket server
├── frontend/
│   ├── dispatch_dashboard.py  # Main Streamlit dashboard
│   ├── rider_map.py           # Map visualization
│   ├── metrics_panel.py       # Metrics display
│   └── websocket_client.py    # WebSocket client helper
└── start_dispatch_system.sh   # Startup script
```

## Quick Start

### Option 1: Use Startup Script (Easiest)

```bash
cd prepsense
./start_dispatch_system.sh
```

This will:
1. Start FastAPI backend on port 8000
2. Start Streamlit frontend on port 8504
3. Open browser automatically

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd prepsense/backend
uvicorn websocket_server:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd prepsense
streamlit run frontend/dispatch_dashboard.py --server.port 8504
```

Then open: http://localhost:8504

## Features

### Dispatch Optimization Model

- **Predicted Preparation Completion**: `Tp_pred = mu_T`
- **Prediction Uncertainty**: `sigma_T`
- **Confidence Interval**: `KPT = mu_T ± z*sigma_T`
- **Optimal Assignment**: `T_assign* = mu_T + k*sigma_T - T_travel`

Where `k = (C1 - C2) / (C1 + C2)` based on cost ratio.

### Cost Function

```
Cost = C1 * Idle + C2 * Delay
```

- **C1**: Rider idle cost (default: 1.0)
- **C2**: Delivery delay cost (default: 2.0)

### Real-Time Events

The system generates:
- `ORDER_CREATED` - New order placed
- `KPT_PREDICTED` - Kitchen prep time predicted
- `RIDER_DISPATCHED` - Rider assigned to order
- `RIDER_MOVED` - Rider traveling to restaurant
- `RIDER_ARRIVED` - Rider arrived at restaurant
- `ORDER_PICKED_UP` - Order picked up and completed

### WebSocket Message Format

```json
{
  "event_type": "RIDER_DISPATCHED",
  "order_id": "ORD_0001821",
  "timestamp": "2026-03-11T02:00:00",
  "predicted_kpt": 11.4,
  "confidence": 2.0,
  "dispatch_time": 7.1,
  "travel_time": 4.2,
  "idle_risk": 0.15,
  "delay_risk": 0.10
}
```

## Dashboard Features

### Live Dispatch Panel

- **Predicted KPT**: Kitchen preparation time prediction
- **Confidence Interval**: Uncertainty bounds
- **Optimal Dispatch Time**: Calculated assignment time
- **Idle Risk**: Probability of rider waiting
- **Delay Risk**: Probability of delivery delay

### Dispatch Visualization

- **Restaurants**: Red square markers
- **Available Riders**: Green circle markers
- **Busy Riders**: Orange circle markers
- **Active Dispatches**: Dashed lines connecting riders to restaurants

### Live Metrics

- **Average Rider Idle Time**: Aggregated idle time
- **Dispatch Efficiency**: Overall efficiency score
- **Delivery Delay Probability**: Risk of delays
- **Total Orders**: Orders processed
- **Active Dispatches**: Currently active assignments

## API Endpoints

### WebSocket

- **Endpoint**: `ws://localhost:8000/ws/dispatch`
- **Update Frequency**: Every 200ms
- **Protocol**: JSON messages

### HTTP

- **Health Check**: `GET http://localhost:8000/health`
- **Root**: `GET http://localhost:8000/`

## Configuration

### Backend Configuration

Edit `backend/dispatch_engine.py`:
```python
dispatch_engine = DispatchEngine(
    cost_idle=1.0,    # Rider idle cost
    cost_delay=2.0    # Delivery delay cost
)
```

### Frontend Configuration

Edit `frontend/dispatch_dashboard.py`:
```python
WEBSOCKET_URL = "ws://localhost:8000/ws/dispatch"
```

## Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

Key packages:
- `fastapi>=0.104.0`
- `uvicorn[standard]>=0.24.0`
- `websockets>=12.0`
- `streamlit>=1.28.0`
- `plotly>=5.17.0`
- `numpy>=1.24.0`
- `pandas>=2.0.0`

## Troubleshooting

### WebSocket Connection Failed

1. Make sure backend is running: `uvicorn websocket_server:app --reload`
2. Check port 8000 is not blocked
3. Verify WebSocket URL in frontend matches backend

### Frontend Not Updating

1. Check WebSocket connection status (should show "🟢 Connected")
2. Verify backend is sending events (check backend logs)
3. Try refreshing the page

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 8504
lsof -ti:8504 | xargs kill -9
```

## Integration with Existing PrepSense

The Dispatch Engine integrates seamlessly with the existing PrepSense system:

1. Uses KPT predictions from `prediction_service.py`
2. Leverages dispatch optimization from `dispatch_optimizer.py`
3. Extends visualization with real-time map updates
4. Complements existing dashboard pages

## Next Steps

- Add persistent storage for dispatch history
- Implement rider availability prediction
- Add multi-restaurant optimization
- Integrate with actual telemetry data
- Deploy to production infrastructure
