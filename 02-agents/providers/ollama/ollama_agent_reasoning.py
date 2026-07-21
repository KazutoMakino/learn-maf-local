# Copyright (c) Microsoft. All rights reserved.

import asyncio

from agent_framework import Agent
from agent_framework.ollama import OllamaChatClient

"""
Ollama Agent Reasoning Example

OllamaChatClient の推論（reasoning/thinking）モードを有効化するサンプル。
gemma4:12b-it-qat は thinking capability に対応しているため、他のサンプルと同じモデルで動作する。
"""


async def main() -> None:
    print("=== Response Reasoning Example ===")

    agent = Agent(
        client=OllamaChatClient(
            host="http://localhost:11434", model="gemma4:12b-it-qat", additional_properties=120.0
        ),
        name="TimeAgent",
        instructions="You are a helpful agent answer in one sentence.",
        default_options={"think": True},  # エージェントレベルで推論を有効化
    )
    query = "Hey what is 3+4? Can you explain how you got to that answer?"
    print(f"User: {query}")
    result = await agent.run(query)
    reasoning = "".join((c.text or "") for c in result.messages[-1].contents if c.type == "text_reasoning")
    print(f"Reasoning: {reasoning}")
    print(f"Answer: {result}\n")


if __name__ == "__main__":
    asyncio.run(main())
