from datetime import timedelta

import pytest
import pytest_asyncio
from django.utils import timezone

from src.infrastructure.db.models import Chat, Member, Message
from src.infrastructure.db.repositories.message import MessageRepository


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestMessageRepository:
    @pytest_asyncio.fixture
    async def user(self):
        return await Member.objects.acreate(username="tester", password="123")

    @pytest_asyncio.fixture
    async def chat(self, user):
        chat = await Chat.objects.acreate(name="Test Chat", description="desc", owner=user)
        await chat.members.aadd(user)
        return chat

    @pytest_asyncio.fixture
    def repo(self):
        return MessageRepository()

    async def test_create_message(self, repo, user, chat):
        content = "Hello world!"
        msg = await repo.create(user.id, chat.id, content)

        assert msg.member_id == user.id
        assert msg.chat_id == chat.id
        assert msg.content == content
        assert msg.username == user.username
        assert await Message.objects.filter(id=msg.id).aexists()

    async def test_list_recent_messages(self, repo, user, chat):
        for i in range(5):
            await Message.objects.acreate(
                member=user,
                chat=chat,
                content=f"Message {i}",
                created_at=timezone.now() - timedelta(minutes=i),
            )

        result = await repo.list_recent(chat.id, offset=0, limit=5)

        assert len(result) == 5
        assert result[0].content == "Message 0"
        assert result[-1].content == "Message 4"
