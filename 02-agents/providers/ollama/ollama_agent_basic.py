# Copyright (c) Microsoft. All rights reserved.

import asyncio
from datetime import datetime

from agent_framework import Agent, tool
from agent_framework.ollama import OllamaChatClient

"""
Ollama Agent Basic Example

OllamaChatClient を使ってローカルの Ollama モデルでツール呼び出しを行う最小構成のサンプル。
非ストリーミング／ストリーミング両方のレスポンス取得方法を示す。

事前に Ollama をインストールし、モデル（例: gemma4:12b-it-qat）を pull した上で
ローカルで起動しておくこと（https://ollama.com/）。
"""


# NOTE: approval_mode="never_require" is for sample brevity. Use "always_require" in production;
# see samples/02-agents/tools/function_tool_with_approval.py
# and samples/02-agents/tools/function_tool_with_approval_and_sessions.py.
@tool(approval_mode="never_require")
def get_time(location: str) -> str:
    """Get the current time."""
    return f"The current time in {location} is {datetime.now().strftime('%I:%M %p')}."


async def non_streaming_example() -> None:
    """Example of non-streaming response (get the complete result at once)."""
    print("=== Non-streaming Response Example ===")

    agent = Agent(
        client=OllamaChatClient(
            host="http://localhost:11434", model="gemma4:12b-it-qat", additional_properties=120.0
        ),
        name="TimeAgent",
        instructions="You are a helpful time agent answer in one sentence.",
        tools=get_time,
    )

    query = "What time is it in Seattle? Use a tool call"
    print(f"User: {query}")
    result = await agent.run(query)
    print(f"Result: {result}\n")


async def streaming_example() -> None:
    """Example of streaming response (get results as they are generated)."""
    print("=== Streaming Response Example ===")

    agent = Agent(
        client=OllamaChatClient(
            host="http://localhost:11434", model="gemma4:12b-it-qat", additional_properties=120.0
        ),
        name="TimeAgent",
        instructions="You are a helpful time agent answer in one sentence.",
        tools=get_time,
    )
    query = "What time is it in San Francisco? Use a tool call"
    print(f"User: {query}")
    print("Agent: ", end="", flush=True)
    async for chunk in agent.run(query, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print("\n")


async def main() -> None:
    print("=== Basic Ollama Chat Client Agent Example ===")

    await non_streaming_example()
    await streaming_example()


if __name__ == "__main__":
    asyncio.run(main())
