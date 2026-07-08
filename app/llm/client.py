import json
from typing import Any, cast

from openai import OpenAI
from openai.types.chat import ChatCompletionFunctionToolParam

from app.chat.memory import memory
from app.core.config import settings
from app.llm.schemas import LLMChatResponse
from app.tools.calculator import add_numbers

if settings.OPENAI_API_KEY is None:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an experienced AI Engineering mentor.

Return a clear, practical answer.
Detect the topic of the user's question.
Set confidence from 0 to 1.

If the user asks to add numbers, use the add_numbers tool.
"""

TOOLS: list[ChatCompletionFunctionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two numbers and return the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    }
]


def ask_llm(session_id: str, prompt: str) -> LLMChatResponse:
    conversation = memory[session_id]

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *conversation,
        {"role": "user", "content": prompt},
    ]

    first_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=cast(Any, messages),
        tools=TOOLS,
        tool_choice="auto",
    )

    first_message = first_response.choices[0].message

    if first_message.tool_calls:
        tool_call = cast(Any, first_message.tool_calls[0])

        if tool_call.function.name != "add_numbers":
            raise RuntimeError("Unknown tool call")

        arguments = json.loads(tool_call.function.arguments)

        tool_result = add_numbers(
            a=arguments["a"],
            b=arguments["b"],
        )

        messages_with_tool_result = [
            *messages,
            first_message,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_result),
            },
        ]

        final_response = client.responses.parse(
            model="gpt-4.1-mini",
            input=cast(Any, messages_with_tool_result),
            text_format=LLMChatResponse,
        )

        parsed = final_response.output_parsed

        if parsed is None:
            raise RuntimeError("LLM returned empty structured response")

        conversation.append({"role": "user", "content": prompt})
        conversation.append({"role": "assistant", "content": parsed.answer})

        return parsed

    parsed_response = client.responses.parse(
        model="gpt-4.1-mini",
        input=cast(Any, messages),
        text_format=LLMChatResponse,
    )

    parsed = parsed_response.output_parsed

    if parsed is None:
        raise RuntimeError("LLM returned empty structured response")

    conversation.append({"role": "user", "content": prompt})
    conversation.append({"role": "assistant", "content": parsed.answer})

    return parsed
