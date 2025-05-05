from entities.message import MessageEntity
from pydantic import BaseModel


class MessagePresenter(BaseModel):
    member_id: int
    chat_id: int
    content: str
    created_at: str

    @classmethod
    def from_entity(cls, entity: MessageEntity) -> "MessagePresenter":
        return cls(
            member_id=entity.member_id,
            chat_id=entity.chat_id,
            content=entity.content,
            created_at=entity.created_at.isoformat(),
        )

    def to_dict(self) -> dict:
        return self.model_dump()
