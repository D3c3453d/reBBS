# src/interface/repositories/message.py
from typing import Protocol, runtime_checkable


@runtime_checkable
class ChatRepositoryProtocol(Protocol):
    async def create(self, owner_id: int, name: str, description: str) -> None:
        pass

    async def subscribe(self, user_id: int, chat_id: int) -> None:
        pass

    async def unsubscribe(self, user_id: int, chat_id: int) -> None:
        pass

    async def is_subscribed(self, user_id: int, chat_id: int) -> bool:
        pass
