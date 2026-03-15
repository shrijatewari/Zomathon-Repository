#!/bin/bash

# Alternative: Using localtunnel (no signup required, but URLs change each time)
# Install: npm install -g localtunnel

PORT=8504

echo "🚀 Starting localtunnel for PrepSense dashboard..."
echo "📡 Make sure Streamlit is running on port $PORT"
echo ""

if command -v lt &> /dev/null; then
    echo "🌐 Your shareable URL will appear below:"
    echo ""
    lt --port $PORT
else
    echo "❌ localtunnel not found."
    echo ""
    echo "To install:"
    echo "  1. Install Node.js: https://nodejs.org/"
    echo "  2. Run: npm install -g localtunnel"
    echo "  3. Then run this script again"
    echo ""
    echo "Or use ngrok instead (see share_dashboard.sh)"
fi
