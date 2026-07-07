from litellm import completion
from app.core.config import settings

import os

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


def ask_llm(prompt: str):

    response = completion(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content