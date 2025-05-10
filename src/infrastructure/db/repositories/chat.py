# src/infrastructure/db/repositories/chat.py

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

from src.entities.message import MessageEntity
from src.infrastructure.db.models import Message as MessageModel
from src.interface.repositories.chat import ChatRepository

Member = get_user_model()


class DjangoChatRepository(ChatRepository):
    async def save(self, member_id: int, chat_id: int, content: str) -> MessageEntity:
        message = await MessageModel.objects.acreate(
            member_id=member_id,
            chat_id=chat_id,
            content=content,
        )
        member = await Member.objects.aget(id=member_id)
        return MessageEntity(
            id=message.id,
            member_id=message.member_id,
            chat_id=message.chat_id,
            content=message.content,
            created_at=message.created_at,
            username=member.username,
        )

    @sync_to_async
    def _sync_list_recent(self, chat_id: int, limit: int):
        # Returns a normal Python list of model instances
        return list(
            MessageModel.objects.select_related("member").filter(chat_id=chat_id).order_by("-created_at")[:limit]
        )

    async def list_recent(self, chat_id: int, limit: int) -> list[MessageEntity]:
        # Fetch the rows in a thread, then map to entities
        messages = await self._sync_list_recent(chat_id, limit)
        # Reverse so oldest → newest
        return [
            MessageEntity(
                id=message.id,
                member_id=message.member_id,
                chat_id=message.chat_id,
                content=message.content,
                created_at=message.created_at,
                username=message.member.username,
            )
            for message in reversed(messages)
        ]
