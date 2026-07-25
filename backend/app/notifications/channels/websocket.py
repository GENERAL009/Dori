from app.notifications.channels.base import NotificationChannel


class WebSocketNotificationChannel(NotificationChannel):
    async def send(self, user_id: str, title: str, message: str, data: dict = None) -> bool:
        from app.notifications.manager import connection_manager

        if not connection_manager.is_connected(user_id):
            return False

        payload = {
            "type": "medication_reminder",
            "title": title,
            "message": message,
            "data": data or {},
            "actions": ["taken", "skipped", "snoozed"],
        }
        await connection_manager.send_notification(user_id, payload)
        return True

    async def is_available(self, user_id: str) -> bool:
        from app.notifications.manager import connection_manager
        return connection_manager.is_connected(user_id)
