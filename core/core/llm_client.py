import json
from openai import OpenAI


class LLMClient:
    def __init__(self, model: str = "gpt-4.1", temperature: float = 0.0):
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature

    def generate(self, messages: list[dict]) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("LLM response is not valid JSON")
