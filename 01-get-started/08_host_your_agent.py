# Copyright (c) Microsoft. All rights reserved.

from typing import Any

from agent_framework import Agent
from agent_framework.azure import AgentFunctionApp
from agent_framework.ollama import OllamaChatClient

"""Host your agent with Azure Functions.
This sample shows the Python hosting pattern used in docs:
- Create an agent with `FoundryChatClient`
- Register it with `AgentFunctionApp`
- Run with Azure Functions Core Tools (`func start`)
Prerequisites:
  pip install agent-framework-azurefunctions --pre
"""


# <create_agent>
def _create_agent() -> Any:
    """Create a hosted agent backed by Azure OpenAI."""
    return Agent(
        client=OllamaChatClient(
            host="http://localhost:11434",
            model="gemma4:e2b",
            additional_properties=120.0,
        ),
        name="HostedAgent",
        instructions="You are a helpful assistant hosted in Azure Functions.",
    )


# </create_agent>
# <host_agent>
app = AgentFunctionApp(agents=[_create_agent()], enable_health_check=True, max_poll_retries=50)
# </host_agent>
if __name__ == "__main__":
    print("Start the Functions host with: func start")
    print("Then call: POST /api/agents/HostedAgent/run")
