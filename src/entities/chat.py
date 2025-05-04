from dataclasses import dataclass


@dataclass(frozen=True)
class ChatEntity:
    id: int
    name: str
    is_group: bool
