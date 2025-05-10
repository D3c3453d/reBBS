# src/infrastructure/db/repositories/message.py
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

from src.entities.message import MessageEntity
from src.infrastructure.db.models import Message
from src.interface.repositories.message import MessageRepositoryProtocol

Member = get_user_model()


class MessageRepository(MessageRepositoryProtocol):
    async def save(self, member_id: int, chat_id: int, content: str) -> MessageEntity:
        message = await Message.objects.acreate(
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
    def _sync_list_recent(self, chat_id: int, offset: int, limit: int):
        # Returns a normal Python list of model instances
        return list(
            Message.objects.select_related("member").filter(chat_id=chat_id).order_by("-created_at")[offset:limit]
        )

    async def list_recent(self, chat_id: int, offset: int, limit: int) -> list[MessageEntity]:
        # Fetch the rows in a thread, then map to entities
        messages = await self._sync_list_recent(chat_id, offset, limit)
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
