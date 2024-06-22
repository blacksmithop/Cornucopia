import logging

from fastapi import APIRouter

from utils.agent_with_memory import agent_with_chat_history as agent
from utils.schemas import ChatMessage

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/chat", tags=["Chat"])
async def chat_with_ai(payload: ChatMessage):
    session_id = payload.session_id
    message = payload.message

    response = agent.invoke(
        {"input": message},
        config={"configurable": {"session_id": session_id}},
    )

    output = response["output"]
    intermediate_steps = response["intermediate_steps"]

    return {"response": output, "steps": intermediate_steps}
