from litellm import completion
from app.chat.memory import memory
from app.core.config import settings

import os

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


SYSTEM_PROMPT = """
You are an experienced AI Engineering mentor.

Your responsibilities:

- explain concepts clearly
- give concise answers
- provide practical examples
- write clean Python code
- follow FastAPI best practices
"""


def ask_llm(
    session_id: str,
    prompt: str,
):
    
    conversation = memory[session_id]

    response = completion(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        *conversation,
        {
            "role": "user",
            "content": prompt,
        },
    ],
)

    answer = response.choices[0].message.content

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