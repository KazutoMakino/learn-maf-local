# Copyright (c) Microsoft. All rights reserved.

import asyncio

from agent_framework import Agent, AgentSession
from agent_framework.ollama import OllamaChatClient

"""
Session Suspend and Resume Example

This sample demonstrates how to suspend and resume conversation sessions.
Some chat clients (e.g. Azure AI Foundry) support service-managed sessions on
the server side, but OllamaChatClient — like most clients — manages session
state purely in-memory / client-side. This sample shows two equivalent ways
of doing so: via `Agent` used as an async context manager, and via a plain
`Agent` instance.
"""


async def suspend_resume_via_context_manager() -> None:
    """Demonstrates how to suspend and resume a session using Agent as an async context manager."""
    print("=== Suspend-Resume via Async Context Manager ===")

    async with Agent(
        client=OllamaChatClient(host="http://localhost:11434", model="gemma4:12b-it-qat", additional_properties=120.0),
        name="MemoryBot",
        instructions="You are a helpful assistant that remembers our conversation.",
    ) as agent:
        # Start a new session for the agent conversation.
        session = agent.create_session()

        # Respond to user input.
        query = "Hello! My name is Alice and I love pizza."
        print(f"User: {query}")
        print(f"Agent: {await agent.run(query, session=session)}\n")

        # Serialize the session state, so it can be stored for later use.
        serialized_session = session.to_dict()

        # The session can now be saved to a database, file, or any other storage mechanism and loaded again later.
        print(f"Serialized session: {serialized_session}\n")

        # Deserialize the session state after loading from storage.
        resumed_session = AgentSession.from_dict(serialized_session)

        # Respond to user input.
        query = "What do you remember about me?"
        print(f"User: {query}")
        print(f"Agent: {await agent.run(query, session=resumed_session)}\n")


async def suspend_resume_in_memory_session() -> None:
    """Demonstrates how to suspend and resume an in-memory session."""
    print("=== Suspend-Resume In-Memory Session ===")

    agent = Agent(
        client=OllamaChatClient(host="http://localhost:11434", model="gemma4:12b-it-qat", additional_properties=120.0),
        name="MemoryBot",
        instructions="You are a helpful assistant that remembers our conversation.",
    )

    # Start a new session for the agent conversation.
    session = agent.create_session()

    # Respond to user input.
    query = "Hello! My name is Alice and I love pizza."
    print(f"User: {query}")
    print(f"Agent: {await agent.run(query, session=session)}\n")

    # Serialize the session state, so it can be stored for later use.
    serialized_session = session.to_dict()

    # The session can now be saved to a database, file, or any other storage mechanism and loaded again later.
    print(f"Serialized session: {serialized_session}\n")

    # Deserialize the session state after loading from storage.
    resumed_session = AgentSession.from_dict(serialized_session)

    # Respond to user input.
    query = "What do you remember about me?"
    print(f"User: {query}")
    print(f"Agent: {await agent.run(query, session=resumed_session)}\n")


async def main() -> None:
    print("=== Suspend-Resume Session Examples ===")
    await suspend_resume_via_context_manager()
    await suspend_resume_in_memory_session()


if __name__ == "__main__":
    asyncio.run(main())
