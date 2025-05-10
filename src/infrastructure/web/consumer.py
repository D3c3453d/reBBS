# src/infrastructure/web/consumer.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from src.infrastructure.db.repositories.message import MessageRepository
from src.interface.controllers.message import MessageController
from src.usecases.message import GetRecentMessages, MessageUsecases, SendMessage


class Consumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        message_repo = MessageRepository()
        send_message = SendMessage(repo=message_repo)
        get_recent_messages = GetRecentMessages(repo=message_repo)
        self.message_controller = MessageController(
            usecases=MessageUsecases(
                send_message=send_message,
                get_recent_messages=get_recent_messages,
            )
        )

    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.user_id = self.scope["user"].id
        self.group = f"chat_{self.chat_id}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

        # Delegate to controller
        messages = await self.message_controller.load_history(self.chat_id)
        for msg in messages:
            await self.send_json(msg)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive_json(self, content):
        if content.get("type") == "message":
            msg = await self.message_controller.handle_incoming(self.user_id, self.chat_id, content)
            await self.channel_layer.group_send(self.group, {"type": "message", **msg})

    async def message(self, event):
        await self.send_json(event)
