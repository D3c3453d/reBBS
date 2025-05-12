# src/usecases/message.py
from dataclasses import dataclass

from src.entities.message import MessageEntity
from src.interface.repositories.message import MessageRepositoryProtocol


class SendMessage:
    def __init__(self, repo: MessageRepositoryProtocol):
        self.repo = repo

    async def execute(self, member_id: int, chat_id: int, content: str) -> MessageEntity:
        return await self.repo.create(member_id, chat_id, content)


class GetRecentMessages:
    def __init__(self, repo: MessageRepositoryProtocol):
        self.repo = repo

    async def execute(self, chat_id: int, offset: int = 0, limit: int = 50) -> list[MessageEntity]:
        return await self.repo.list_recent(chat_id, offset, limit)


@dataclass
class MessageUsecases:
    send_message: SendMessage | None = None
    get_recent_messages: GetRecentMessages | None = None
