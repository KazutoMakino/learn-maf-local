# Copyright (c) Microsoft. All rights reserved.

import asyncio

from agent_framework import Agent
from agent_framework.ollama import OllamaChatClient

"""
Hello Agent — Simplest possible agent

This sample creates a minimal agent using FoundryChatClient via an
Azure AI Foundry project endpoint, and runs it in both non-streaming and streaming modes.

There are XML tags in all of the get started samples, those are used to display the same code in the docs repo.
"""


async def main() -> None:
    client = OllamaChatClient(host="http://localhost:11434", model="gemma4:e2b")

    agent = Agent(
        client=client, name="HelloAgent", instructions="You are a friendly assistant. Keep your answers brief."
    )

    result = await agent.run("What is the capital of France?")
    print(f"Agent: {result}")

    print("Agent (streaming): ", end="", flush=True)
    async for chunk in agent.run("Tell me a one-sentence fun fact.", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
