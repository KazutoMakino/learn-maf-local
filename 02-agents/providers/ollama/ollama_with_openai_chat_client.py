# Copyright (c) Microsoft. All rights reserved.

import asyncio
from random import randint
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.openai import OpenAIChatClient

"""
Ollama with OpenAI Chat Client Example

Ollama は OpenAI 互換の API エンドポイント（/v1/）も提供しているため、
OllamaChatClient の代わりに OpenAIChatClient の base_url をローカルの Ollama サーバーに
向けることでも利用できる。OpenAI クライアントの流儀に慣れている場合の代替手段として紹介する。
"""


# NOTE: approval_mode="never_require" is for sample brevity. Use "always_require" in production;
# see samples/02-agents/tools/function_tool_with_approval.py
# and samples/02-agents/tools/function_tool_with_approval_and_sessions.py.
@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, "The location to get the weather for."],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


async def non_streaming_example() -> None:
    """Example of non-streaming response (get the complete result at once)."""
    print("=== Non-streaming Response Example ===")

    _client = OpenAIChatClient(
        api_key="ollama",  # ダミー値。Ollama は API キーを必要としない
        base_url="http://localhost:11434/v1/",
        model="gemma4:12b-it-qat",
    )
    agent = Agent(
        client=_client,
        name="WeatherAgent",
        instructions="You are a helpful weather agent.",
        tools=[get_weather],
    )

    query = "What's the weather like in Seattle?"
    print(f"User: {query}")
    result = await agent.run(query)
    print(f"Agent: {result}\n")


async def streaming_example() -> None:
    """Example of streaming response (get results as they are generated)."""
    print("=== Streaming Response Example ===")

    _client = OpenAIChatClient(
        api_key="ollama",  # ダミー値。Ollama は API キーを必要としない
        base_url="http://localhost:11434/v1/",
        model="gemma4:12b-it-qat",
    )
    agent = Agent(
        client=_client,
        name="WeatherAgent",
        instructions="You are a helpful weather agent.",
        tools=[get_weather],
    )

    query = "What's the weather like in Portland?"
    print(f"User: {query}")
    print("Agent: ", end="", flush=True)
    async for chunk in agent.run(query, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print("\n")


async def main() -> None:
    print("=== Ollama with OpenAI Chat Client Agent Example ===")

    await non_streaming_example()
    await streaming_example()


if __name__ == "__main__":
    asyncio.run(main())
