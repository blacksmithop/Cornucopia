from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory


message_store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in message_store:
        message_store[session_id] = ChatMessageHistory()
    return message_store[session_id]
