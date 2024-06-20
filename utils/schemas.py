from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str
    session_id: str