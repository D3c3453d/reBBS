# src/interface/controllers/message.py
from src.interface.presenters.message import MessagePresenter
from src.usecases.message import MessageUsecases


class MessageController:
    def __init__(self, usecases: MessageUsecases):
        self.usecases = usecases

    async def load_history(self, chat_id: int) -> list[dict]:
        messages = await self.usecases.get_recent_messages.execute(chat_id)
        return [MessagePresenter.from_entity(m).to_dict() for m in messages]

    async def handle_incoming(self, user_id: int, chat_id: int, payload: dict) -> dict:
        msg = await self.usecases.send_message.execute(
            member_id=user_id,
            chat_id=chat_id,
            content=payload["content"],
        )
        return MessagePresenter.from_entity(msg).to_dict()
