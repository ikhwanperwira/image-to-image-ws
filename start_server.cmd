@echo off
echo Starting WebSocket Server...
start "" python ws_server.py
echo WebSocket Server started.

echo Starting HTTP Server...
start "" python http_server.py
echo HTTP Server started.
