import pytest
import pytest_asyncio

from src.infrastructure.db.models import Chat, Member, MemberChat
from src.infrastructure.db.repositories.chat import ChatRepository


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestChatRepository:
    @pytest_asyncio.fixture
    async def user(self):
        return await Member.objects.acreate(username="subscriber", password="testpass")

    @pytest_asyncio.fixture
    def repo(self):
        return ChatRepository()

    @pytest.mark.asyncio
    async def test_create_chat(self, repo, user):
        await repo.create(owner_id=user.id, name="Cool Chat", description="Some desc")
        chat_exists = await Chat.objects.filter(name="Cool Chat", owner=user).aexists()
        assert chat_exists

    @pytest.mark.asyncio
    async def test_subscribe_unsubscribe_and_check(self, repo, user):
        chat = await Chat.objects.acreate(name="Sub Chat", description="desc", owner=user)

        assert await repo.is_subscribed(user.id, chat.id) is False

        await repo.subscribe(user.id, chat.id)
        assert await repo.is_subscribed(user.id, chat.id)

        memberchat_exists = await MemberChat.objects.filter(member=user, chat=chat).aexists()
        assert memberchat_exists

        await repo.unsubscribe(user.id, chat.id)
        assert await repo.is_subscribed(user.id, chat.id) is False
