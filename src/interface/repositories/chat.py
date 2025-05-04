from abc import ABC, abstractmethod
from typing import List

from src.entities.message import MessageEntity


class ChatRepository(ABC):
    @abstractmethod
    async def save(self, member_id: int, chat_id: int, content: str) -> MessageEntity:
        ...

    @abstractmethod
    async def list_recent(self, chat_id: int, limit: int) -> List[MessageEntity]:
        ...
