from collections import deque
from config import settings
from llm.ollama_client import OllamaClient
from typing import Optional
import time


class BaseAgent:

    def __init__(self, name: str, role_prompt: str, model: str, event_bus: Optional[object] = None, memory_manager=None, temperature: float = 0.2,
    num_predict: int = 400,):
        self.name = name
        self.role_prompt = role_prompt
        self.model = model
        self.event_bus = event_bus
        self.memory_manager = memory_manager

        self.history = deque(maxlen=settings.agent.memory_window)
        self.temperature = temperature
        self.num_predict = num_predict

    def build_messages(
        self,
        user_input: str,
        context: str | None = None,
    ) -> list[dict]:

        messages = [
            {
                "role": "system",
                "content": self.role_prompt,
            }
        ]

        memory_context = ""

        should_retrieve = (
            context is None
            and self.memory_manager is not None
        )

        if self.memory_manager and should_retrieve:
            memory_context = self.memory_manager.build_context(user_input)

            if memory_context:
                print("\nRetrieved Memories:")
                print(memory_context)

        final_user_message = ""

        if memory_context:
            final_user_message += (
                f"Relevant Memory:\n{memory_context}\n\n"
            )

        if context:
            final_user_message += (
                f"Context:\n{context}\n\n"
            )

        final_user_message += (
            f"User Question:\n{user_input}"
        )

        messages.extend(self.history)

        print("FINAL USER MESSAGE:")
        print(repr(final_user_message))

        messages.append(
            {
                "role": "user",
                "content": final_user_message,
            }
        )

        return messages

    def _update_history(
        self,
        user_input: str,
        response: str,
    ) -> None:

        self.history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        self.history.append(
            {
                "role": "assistant",
                "content": response,
            }
        )
        MAX_HISTORY = 8

        if len(self.history) > MAX_HISTORY:
            self.history = self.history[-MAX_HISTORY:]

    async def think(self, user_input: str, context: str | None = None, execution_context=None):

        start = time.perf_counter()

        

        if self.event_bus:
            await self.event_bus.publish(
                "agent started",
                {
                    "agent": self.name,
                    "input": user_input,
                }
            )

        print(f"\n[{self.name}] Started")

        try:

            messages = self.build_messages(
                user_input,
                context,
            )

            response = await OllamaClient.chat(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                num_predict=self.num_predict,
            )

            self._update_history(
                user_input,
                response,
            )

            
            if execution_context:
                execution_context.put(
                    f"{self.name}_output",
                    response,
                )

            return response

        except Exception as e:
            raise

        finally:

            if self.event_bus:
                await self.event_bus.publish(
                    "agent finished",
                    {
                        "agent": self.name,
                        "output": locals().get("response"),
                    }
                )

            end = time.perf_counter()

            print(f"[{self.name}] Finished")
            print(f"{self.name} took {end-start:.2f} sec")