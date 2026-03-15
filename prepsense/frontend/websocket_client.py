"""
WebSocket Client Helper for Streamlit

Since Streamlit doesn't support async WebSocket clients directly,
this module provides a thread-based client that updates session state.
"""

import threading
import websockets
import asyncio
import json
from typing import Callable, Optional
from datetime import datetime


class StreamlitWebSocketClient:
    """
    WebSocket client that runs in a separate thread and calls a callback
    function when messages are received.
    """
    
    def __init__(self, url: str, on_message: Callable[[dict], None]):
        """
        Initialize WebSocket client.
        
        Parameters:
        -----------
        url : str
            WebSocket URL (e.g., "ws://localhost:8000/ws/dispatch")
        on_message : Callable[[dict], None]
            Callback function called when a message is received
        """
        self.url = url
        self.on_message = on_message
        self.thread: Optional[threading.Thread] = None
        self.running = False
        self.connected = False
    
    def start(self):
        """Start WebSocket client in background thread."""
        if self.running:
            return
        
        self.running = True
        self.connected = False  # Reset connection status
        
        # Stop old thread if exists
        if self.thread and self.thread.is_alive():
            self.running = False
            self.thread.join(timeout=1.0)
        
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        
        # Give thread a moment to start connecting
        import time
        time.sleep(0.5)  # Increased wait time
    
    def stop(self):
        """Stop WebSocket client."""
        self.running = False
    
    def _run(self):
        """Run WebSocket client (called in thread)."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self._connect())
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            loop.close()
    
    async def _connect(self):
        """Connect to WebSocket and receive messages."""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries and self.running:
            try:
                async with websockets.connect(
                    self.url,
                    ping_interval=20,
                    ping_timeout=10,
                    close_timeout=10
                ) as websocket:
                    self.connected = True
                    print(f"✅ Connected to {self.url}")
                    retry_count = 0  # Reset on successful connection
                    
                    while self.running:
                        try:
                            message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                            data = json.loads(message)
                            self.on_message(data)
                        except asyncio.TimeoutError:
                            # Send ping to keep connection alive
                            try:
                                await websocket.ping()
                            except:
                                break
                        except websockets.exceptions.ConnectionClosed:
                            print("WebSocket connection closed")
                            self.connected = False
                            break
                        except json.JSONDecodeError:
                            # Skip invalid JSON
                            continue
                            
            except Exception as e:
                retry_count += 1
                print(f"WebSocket connection error (attempt {retry_count}/{max_retries}): {e}")
                self.connected = False
                if retry_count < max_retries:
                    await asyncio.sleep(2)  # Wait before retry
                else:
                    print("Max retries reached. WebSocket connection failed.")
                    break
        
        # Set disconnected when loop exits
        self.connected = False
        print("WebSocket client stopped")


# Global client instance
_client: Optional[StreamlitWebSocketClient] = None


def get_websocket_client(url: str, on_message: Callable[[dict], None]) -> StreamlitWebSocketClient:
    """
    Get or create WebSocket client singleton.
    
    Parameters:
    -----------
    url : str
        WebSocket URL
    on_message : Callable[[dict], None]
        Callback for messages
    
    Returns:
    --------
    StreamlitWebSocketClient
        WebSocket client instance
    """
    global _client
    
    # Always create new client for Streamlit (session state handles persistence)
    _client = StreamlitWebSocketClient(url, on_message)
    _client.start()
    
    return _client
