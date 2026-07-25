from abc import ABC, abstractmethod
from typing import Any


class NotificationChannel(ABC):
    @abstractmethod
    async def send(self, user_id: str, title: str, message: str, data: dict = None) -> bool:
        pass

    @abstractmethod
    async def is_available(self, user_id: str) -> bool:
        pass
