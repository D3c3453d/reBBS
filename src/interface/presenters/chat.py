from entities.message import MessageEntity


def message_to_dict(msg: MessageEntity) -> dict:
    return {
        "id": msg.id,
        "member_id": msg.member_id,
        "chat_id": msg.chat_id,
        "content": msg.content,
        "created_at": msg.created_at.isoformat(),
    }
