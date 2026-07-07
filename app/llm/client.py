from openai import OpenAI

from app.chat.memory import memory
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an experienced AI Engineering mentor.

Your responsibilities:

- explain concepts clearly
- give concise answers
- provide practical examples
- write clean Python code
- follow FastAPI best practices
"""


def ask_llm(session_id: str, prompt: str) -> str:
    conversation = memory[session_id]

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        *conversation,
        {
            "role": "user",
            "content": prompt,
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )

    answer = response.choices[0].message.content

    if answer is None:
        raise RuntimeError("Empty response")

    conversation.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    conversation.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    return answer
