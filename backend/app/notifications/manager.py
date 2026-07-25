import json
from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def send_notification(self, user_id: str, notification: dict):
        websocket = self.active_connections.get(user_id)
        if websocket:
            try:
                await websocket.send_json({
                    "type": "notification",
                    "data": notification,
                })
            except Exception:
                self.disconnect(user_id)

    async def broadcast(self, message: dict):
        disconnected = []
        for user_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception:
                disconnected.append(user_id)
        for user_id in disconnected:
            self.disconnect(user_id)

    def is_connected(self, user_id: str) -> bool:
        return user_id in self.active_connections


connection_manager = ConnectionManager()
