from django.utils import timezone

from src.entities.message import MessageEntity
from src.infrastructure.db.models import Message as MessageModel
from src.interface.repositories.chat import ChatRepository


class DjangoChatRepository(ChatRepository):
    async def save(self, member_id: int, chat_id: int, content: str) -> MessageEntity:
        obj = MessageModel.objects.create(
            member_id=member_id, chat_id=chat_id, content=content, created_at=timezone.now()
        )
        return MessageEntity(
            id=obj.id, member_id=obj.member_id, chat_id=obj.chat_id, content=obj.content, created_at=obj.created_at
        )

    async def list_recent(self, chat_id: int, limit: int) -> list[MessageEntity]:
        rows = MessageModel.objects.filter(chat_id=chat_id).order_by("-created_at")[:limit]
        return [
            MessageEntity(
                id=row.id, member_id=row.member_id, chat_id=row.chat_id, content=row.content, created_at=row.created_at
            )
            for row in reversed(rows)
        ]
