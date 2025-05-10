# src/interface/repositories/message.py
from typing import Protocol, runtime_checkable

from src.entities.message import MessageEntity


@runtime_checkable
class MessageRepositoryProtocol(Protocol):
    async def save(self, member_id: int, chat_id: int, content: str) -> MessageEntity:
        pass

    async def list_recent(self, chat_id: int, offset: int, limit: int) -> list[MessageEntity]:
        pass
