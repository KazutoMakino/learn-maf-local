# Copyright (c) Microsoft. All rights reserved.

import asyncio
from datetime import datetime

from agent_framework import Message, tool
from agent_framework.ollama import OllamaChatClient

"""
Ollama Chat Client Example

Agent を介さず、OllamaChatClient を直接使ってツール呼び出し付きの応答を取得するサンプル。
"""


# NOTE: approval_mode="never_require" is for sample brevity. Use "always_require" in production;
# see samples/02-agents/tools/function_tool_with_approval.py
# and samples/02-agents/tools/function_tool_with_approval_and_sessions.py.
@tool(approval_mode="never_require")
def get_time():
    """Get the current time."""
    return f"The current time is {datetime.now().strftime('%I:%M %p')}."


async def main() -> None:
    client = OllamaChatClient(host="http://localhost:11434", model="gemma4:12b-it-qat", additional_properties=120.0)
    message = "What time is it? Use a tool call"
    messages = [Message(role="user", contents=[message])]
    stream = False
    print(f"User: {message}")
    if stream:
        print("Assistant: ", end="")
        async for chunk in client.get_response(messages, tools=get_time, stream=True):
            if str(chunk):
                print(str(chunk), end="")
        print("")
    else:
        response = await client.get_response(messages, tools=get_time)
        print(f"Assistant: {response}")


if __name__ == "__main__":
    asyncio.run(main())
