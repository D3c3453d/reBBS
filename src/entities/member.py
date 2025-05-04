from dataclasses import dataclass


@dataclass(frozen=True)
class MemberEntity:
    id: int
    username: str
    online_status: bool
