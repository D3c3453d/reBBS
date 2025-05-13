from asgiref.sync import async_to_sync

from src.usecases.chat import ChatUsecases


class ChatController:
    def __init__(self, usecases: ChatUsecases):
        self.usecases = usecases

    def handle_create_chat(self, owner_id: int, payload: dict) -> None:
        async_to_sync(self.usecases.create_chat.execute)(
            owner_id=owner_id, name=payload["name"], description=payload["description"]
        )

    async def toggle_subscription(self, user_id: int, chat_id: int) -> None:
        if await self.usecases.is_subscribed.execute(user_id, chat_id):
            await self.usecases.unsubscribe.execute(user_id, chat_id)
        else:
            await self.usecases.subscribe.execute(user_id, chat_id)
