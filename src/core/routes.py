from fastapi import APIRouter
from src.app.v1.chat.controller import chat_router

PREFIX = {
    "V1": "/api/v1",
}

v1_router = APIRouter()
v1_router.include_router(chat_router, prefix=PREFIX["V1"], tags=["Chat"])


