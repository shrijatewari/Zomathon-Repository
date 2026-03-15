# 🚀 Quick Start: Dispatch Decision Engine

## Install Dependencies

```bash
cd prepsense
pip3 install -r requirements.txt
```

## Start the System

### Option 1: Automated (Recommended)

```bash
cd prepsense
./start_dispatch_system.sh
```

This starts both backend and frontend automatically.

### Option 2: Manual (Two Terminals)

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

## Access Dashboard

Open your browser: **http://localhost:8504**

## What You'll See

1. **Live Dispatch Map**: Real-time visualization of restaurants, riders, and active orders
2. **Metrics Panel**: Key performance indicators updating in real-time
3. **Active Dispatches**: List of current dispatch decisions with risk metrics
4. **Event Log**: Stream of all dispatch events

## WebSocket Endpoint

- **URL**: `ws://localhost:8000/ws/dispatch`
- **Update Rate**: Every 200ms
- **Format**: JSON messages

## Troubleshooting

**Backend won't start:**
- Check port 8000 is free: `lsof -ti:8000 | xargs kill -9`
- Install dependencies: `pip3 install fastapi uvicorn websockets`

**Frontend shows "Disconnected":**
- Make sure backend is running on port 8000
- Check WebSocket URL in `frontend/dispatch_dashboard.py`

**No events appearing:**
- Wait a few seconds - events generate automatically
- Check backend terminal for errors
- Refresh the frontend page

## Next Steps

- Read `DISPATCH_ENGINE_README.md` for full documentation
- Customize cost parameters in `backend/dispatch_engine.py`
- Adjust simulation rate in `backend/simulation_engine.py`
