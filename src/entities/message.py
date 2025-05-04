from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MessageEntity:
    id: int
    member_id: int
    chat_id: int
    content: str
    created_at: datetime
