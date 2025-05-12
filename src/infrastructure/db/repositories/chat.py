from src.infrastructure.db.models import Chat, MemberChat
from src.interface.repositories.chat import ChatRepositoryProtocol


class ChatRepository(ChatRepositoryProtocol):
    async def create(self, owner_id: int, name: str, description: str) -> None:
        await Chat.objects.acreate(
            name=name,
            description=description,
            owner_id=owner_id,
        )

    async def subscribe(self, user_id: int, chat_id: int) -> None:
        await MemberChat.objects.acreate(member_id=user_id, chat_id=chat_id)

    async def unsubscribe(self, user_id: int, chat_id: int) -> None:
        await MemberChat.objects.filter(member_id=user_id, chat_id=chat_id).adelete()

    async def is_subscribed(self, user_id: int, chat_id: int) -> bool:
        return await MemberChat.objects.filter(member_id=user_id, chat_id=chat_id).aexists()
