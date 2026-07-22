# Copyright (c) Microsoft. All rights reserved.

import asyncio
from typing import Annotated

from agent_framework import Agent, AgentSession, FunctionInvocationContext, tool
from agent_framework.ollama import OllamaChatClient
from pydantic import Field

"""
AI Function with Session Injection Example

This example demonstrates accessing the agent session inside a tool function
via ``FunctionInvocationContext.session``. The session is automatically
available when the agent is invoked with a session.
"""


# Define the function tool with explicit invocation context.
# The context parameter can also be declared as an untyped parameter with the name: ``ctx``.
@tool(approval_mode="never_require")
async def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
    ctx: FunctionInvocationContext,
) -> str:
    """Get the weather for a given location."""
    session = ctx.session
    if session and isinstance(session, AgentSession) and session.service_session_id:
        print(f"Session ID: {session.service_session_id}.")

    return f"The weather in {location} is cloudy."


async def main() -> None:
    agent = Agent(
        client=OllamaChatClient(host="http://localhost:11434", model="gemma4:12b-it-qat", additional_properties=120.0),
        name="WeatherAgent",
        instructions="You are a helpful weather assistant.",
        tools=[get_weather],
    )

    # Create a session
    session = agent.create_session()

    # Run the agent with the session; tools receive it via ctx.session.
    print(f"Agent: {await agent.run('What is the weather in London?', session=session)}")
    print(f"Agent: {await agent.run('What is the weather in Amsterdam?', session=session)}")
    print(f"Agent: {await agent.run('What cities did I ask about?', session=session)}")


if __name__ == "__main__":
    asyncio.run(main())
