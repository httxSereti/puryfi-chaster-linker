from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from models.connection import Connection
from models.connection_manager import manager

router = APIRouter()

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connection = Connection(websocket)
    manager.add(connection)
    print("[WS] New client connected to WebSocket connection on port 8090")
    try:
        while True:
            data = await websocket.receive_bytes()
            await connection.handle_message(data)
    except WebSocketDisconnect:
        manager.remove(connection)
        print("[WS] Client disconnected from WebSocket connection")
