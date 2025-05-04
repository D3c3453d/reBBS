from src.entities.message import MessageEntity
from src.interface.repositories.chat import ChatRepository


class SendMessage:
    def __init__(self, repo: ChatRepository):
        self.repo = repo

    async def execute(self, member_id: int, chat_id: int, content: str) -> MessageEntity:
        return await self.repo.save(member_id, chat_id, content)


class GetRecentMessages:
    def __init__(self, repo: ChatRepository):
        self.repo = repo

    async def execute(self, chat_id: int, limit: int = 50) -> list[MessageEntity]:
        return await self.repo.list_recent(chat_id, limit)
