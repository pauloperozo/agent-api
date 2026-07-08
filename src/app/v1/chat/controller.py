
from fastapi import APIRouter, Depends
from typing import Annotated
from src.app.v1.chat.schemas import (
     ChatRequest, 
     ChatResponse,
)
from src.app.v1.ai.service import AiService
InjectedAiService = Annotated[AiService, Depends(AiService)]

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.post("/", response_model=ChatResponse)
async def chat_enquiry(body: ChatRequest, ai_service: InjectedAiService):
    result = await ai_service.execute_openai(body.enquiry)
    response = ChatResponse(message=result.message)
    print(f"[ChatController] Chat response: {response.message}")
    return response