from dataclasses import dataclass

from src.interface.repositories.chat import ChatRepositoryProtocol


class CreateChat:
    def __init__(self, repo: ChatRepositoryProtocol):
        self.repo = repo

    async def execute(self, owner_id: int, name: str, description: str) -> None:
        return await self.repo.create(owner_id, name, description)


class SubscribeToChat:
    def __init__(self, repo: ChatRepositoryProtocol):
        self.repo = repo

    async def execute(self, user_id: int, chat_id: int) -> None:
        await self.repo.subscribe(user_id, chat_id)


class UnsubscribeFromChat:
    def __init__(self, repo: ChatRepositoryProtocol):
        self.repo = repo

    async def execute(self, user_id: int, chat_id: int) -> None:
        await self.repo.unsubscribe(user_id, chat_id)


class IsSubscribed:
    def __init__(self, repo: ChatRepositoryProtocol):
        self.repo = repo

    async def execute(self, user_id: int, chat_id: int) -> bool:
        return await self.repo.is_subscribed(user_id, chat_id)


@dataclass
class ChatUsecases:
    create_chat: CreateChat | None = None
    subscribe: SubscribeToChat | None = None
    unsubscribe: UnsubscribeFromChat | None = None
    is_subscribed: IsSubscribed | None = None
