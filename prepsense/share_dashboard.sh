#!/bin/bash

# Script to share your PrepSense dashboard publicly
# This creates a public URL that tunnels to your local Streamlit app

PORT=8504

echo "🚀 Starting ngrok tunnel for PrepSense dashboard..."
echo "📡 Make sure Streamlit is running on port $PORT"
echo ""

# Check if ngrok is in current directory or PATH
if [ -f "./ngrok" ]; then
    NGROK_CMD="./ngrok"
elif command -v ngrok &> /dev/null; then
    NGROK_CMD="ngrok"
else
    echo "❌ ngrok not found. Please install it first."
    exit 1
fi

# Check if authtoken is set (optional for basic use)
if [ -z "$NGROK_AUTHTOKEN" ]; then
    echo "⚠️  Note: For a persistent URL, sign up at https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "   Then run: export NGROK_AUTHTOKEN='your_token_here'"
    echo "   Or run: $NGROK_CMD config add-authtoken YOUR_TOKEN"
    echo ""
fi

# Start ngrok tunnel
echo "🌐 Starting tunnel..."
echo "📋 Your shareable URL will appear below:"
echo ""

$NGROK_CMD http $PORT
