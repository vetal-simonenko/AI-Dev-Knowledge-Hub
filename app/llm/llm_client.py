import json
import logging
from typing import Any, cast

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageFunctionToolCall

from app.chat.memory import memory
from app.core.config import Settings
from app.llm.schemas import LLMChatResponse
from app.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an experienced AI Engineering mentor.

Return a clear, practical answer.
Detect the topic of the user's question.
Set confidence from 0 to 1.

Use available tools when the user asks for exact calculations.
"""


class LLMClient:
    def __init__(
        self,
        openai_client: OpenAI,
        tool_registry: ToolRegistry,
        settings: Settings,
    ) -> None:
        self.openai_client = openai_client
        self.tool_registry = tool_registry
        self.settings = settings

    def ask(self, session_id: str, prompt: str) -> LLMChatResponse:
        conversation = memory[session_id]

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation,
            {"role": "user", "content": prompt},
        ]

        logger.info("Sending message to LLM. session_id=%s", session_id)

        first_response = self.openai_client.chat.completions.create(
            model=self.settings.OPENAI_MODEL,
            messages=cast(Any, messages),
            tools=self.tool_registry.to_openai_tools(),
            tool_choice="auto",
        )

        first_message = first_response.choices[0].message

        if first_message.tool_calls:
            logger.info(
                "LLM requested tool calls. session_id=%s tool_calls_count=%s",
                session_id,
                len(first_message.tool_calls),
            )

            tool_results: list[dict[str, Any]] = []

            for raw_tool_call in first_message.tool_calls:
                tool_call = cast(ChatCompletionMessageFunctionToolCall, raw_tool_call)

                arguments = json.loads(tool_call.function.arguments)

                result = self.tool_registry.execute(
                    tool_name=tool_call.function.name,
                    arguments=arguments,
                )

                logger.info(
                    "Tool executed. session_id=%s tool_name=%s",
                    session_id,
                    tool_call.function.name,
                )

                tool_results.append(
                    {
                        "tool_name": tool_call.function.name,
                        "arguments": arguments,
                        "result": result,
                    }
                )

            final_messages = [
                *messages,
                {
                    "role": "system",
                    "content": (
                        "Tool execution results:\n"
                        f"{json.dumps(tool_results, ensure_ascii=False)}"
                    ),
                },
            ]

            final_response = self.openai_client.responses.parse(
                model=self.settings.OPENAI_MODEL,
                input=cast(Any, final_messages),
                text_format=LLMChatResponse,
            )

            parsed = final_response.output_parsed

            if parsed is None:
                raise RuntimeError("LLM returned empty structured response")

            conversation.append({"role": "user", "content": prompt})
            conversation.append({"role": "assistant", "content": parsed.answer})

            return parsed

        parsed_response = self.openai_client.responses.parse(
            model=self.settings.OPENAI_MODEL,
            input=cast(Any, messages),
            text_format=LLMChatResponse,
        )

        parsed = parsed_response.output_parsed

        if parsed is None:
            raise RuntimeError("LLM returned empty structured response")

        conversation.append({"role": "user", "content": prompt})
        conversation.append({"role": "assistant", "content": parsed.answer})

        return parsed
