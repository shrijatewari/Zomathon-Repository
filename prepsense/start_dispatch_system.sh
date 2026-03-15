#!/bin/bash

# Script to start PrepSense Dispatch System
# Starts both backend (FastAPI) and frontend (Streamlit)

echo "🚀 Starting PrepSense Dispatch Decision Engine..."
echo ""

# Check if backend port is available
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8000 is already in use. Stopping existing process..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 2
fi

# Check if frontend port is available
if lsof -Pi :8504 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8504 is already in use. Stopping existing process..."
    lsof -ti:8504 | xargs kill -9 2>/dev/null
    sleep 2
fi

# Start backend
echo "📡 Starting FastAPI backend on port 8000..."
cd "$(dirname "$0")/backend"
python3 -m uvicorn websocket_server:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
echo ""

# Wait for backend to start
sleep 3

# Start frontend
echo "🖥️  Starting Streamlit frontend on port 8504..."
cd "$(dirname "$0")"
python3 -m streamlit run frontend/dispatch_dashboard.py --server.port 8504 &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo ""

# Wait a bit for Streamlit to start
sleep 5

# Open browser
echo "🌐 Opening browser..."
open http://localhost:8504 2>/dev/null || xdg-open http://localhost:8504 2>/dev/null || echo "Please open http://localhost:8504 manually"

echo ""
echo "✅ PrepSense Dispatch System is running!"
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📍 WebSocket: ws://localhost:8000/ws/dispatch"
echo "📍 Frontend Dashboard: http://localhost:8504"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
wait
