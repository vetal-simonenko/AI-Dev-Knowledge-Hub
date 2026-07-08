from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from openai import OpenAI

from app.core.config import Settings, settings
from app.llm.llm_client import LLMClient
from app.services.chat_service import ChatService
from app.tools.registry import ToolRegistry, create_default_tool_registry


def get_settings() -> Settings:
    return settings


@lru_cache
def get_openai_client() -> OpenAI:
    if settings.OPENAI_API_KEY is None:
        raise RuntimeError("OPENAI_API_KEY is not set")

    return OpenAI(api_key=settings.OPENAI_API_KEY)


@lru_cache
def get_tool_registry() -> ToolRegistry:
    return create_default_tool_registry()


def get_llm_client(
    openai_client: Annotated[OpenAI, Depends(get_openai_client)],
    tool_registry: Annotated[ToolRegistry, Depends(get_tool_registry)],
    app_settings: Annotated[Settings, Depends(get_settings)],
) -> LLMClient:
    return LLMClient(
        openai_client=openai_client,
        tool_registry=tool_registry,
        settings=app_settings,
    )


def get_chat_service(
    llm_client: Annotated[LLMClient, Depends(get_llm_client)],
) -> ChatService:
    return ChatService(llm_client=llm_client)
