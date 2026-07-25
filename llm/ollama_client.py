"""
Centralized Ollama communication layer.
Every agent talks to the LLM through this class.
"""
import asyncio
from ollama import AsyncClient
from config import settings

class OllamaClient:
    def __init__(self):
        self.client = AsyncClient(
            host=settings.llm.base_url
        )
    async def chat(
        self,
        model: str,
        messages: list[dict],temperature=None, num_predict=None,
    ) -> str:
        last_error = None
        for attempt in range(settings.llm.retries + 1):
            try:
                print(f"Sending request to model: {model}")
                response = await asyncio.wait_for(
                    self.client.chat(
                        model=model,
                        messages=messages,
                        think=False,
                        options={
                            "temperature": (
                                settings.llm.temperature
                                if temperature is None
                                else temperature
                            ),
                            "num_predict": (
                                400
                                if num_predict is None
                                else num_predict
                            ),
                        },
                    ),
                    timeout=settings.llm.timeout,
                )    
                print(response)
                return response["message"]["content"]
            except Exception as e:
                last_error = repr(e)
                print(
                    f"Attempt {attempt + 1} failed:"
                    f" {last_error}"
                )
                if attempt < settings.llm.retries:
                    await asyncio.sleep(1)
        raise RuntimeError(
            f"Failed to communicate with Ollama: {last_error}"
        )


OllamaClient = OllamaClient()