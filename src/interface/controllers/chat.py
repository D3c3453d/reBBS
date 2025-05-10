# src/interface/controllers/chat.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from infrastructure.db.repositories.chat import DjangoChatRepository
from interface.presenters.chat import MessagePresenter
from usecases.chat import GetRecentMessages, SendMessage


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
        await self.accept()

        # Fetch history and send as JSON
        history = await GetRecentMessages(DjangoChatRepository()).execute(self.chat_id)
        for msg in history:
            await self.send_json(MessagePresenter.from_entity(msg).to_dict())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive_json(self, content):
        message_type = content.get("type")

        if message_type == "message":
            await self.handle_message(content)
        else:
            print(f"Unhandled message type: {message_type}")

    async def handle_message(self, content):
        message_text = content.get("content")
        user_id = self.scope["user"].id

        # Execute use case
        msg = await SendMessage(DjangoChatRepository()).execute(
            member_id=user_id, chat_id=self.chat_id, content=message_text
        )

        # Send validated data to the group
        message_data = MessagePresenter.from_entity(msg).to_dict()
        await self.channel_layer.group_send(self.chat_group_name, {"type": "message", **message_data})

    async def message(self, event):
        await self.send_json(event)
