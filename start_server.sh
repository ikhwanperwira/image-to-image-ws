#!/bin/bash

echo "Starting WebSocket Server..."
python ws_server.py &  # Run WebSocket server in the background

sleep 2  # Wait for 2 seconds to ensure the WebSocket server starts

echo "Starting HTTP Server..."
python http_server.py
