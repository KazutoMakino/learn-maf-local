# Copyright (c) Microsoft. All rights reserved.

import asyncio

from agent_framework import Content, Message
from agent_framework.ollama import OllamaChatClient

"""
Ollama Agent Multimodal Example

OllamaChatClient で画像入力（マルチモーダル）を扱うサンプル。
gemma4:12b-it-qat は vision capability に対応しているため、他のサンプルと同じモデルで動作する。
"""


def create_sample_image() -> str:
    """Create a simple 1x1 pixel PNG image for testing."""
    # This is a tiny red pixel in PNG format
    png_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    return f"data:image/png;base64,{png_data}"


async def test_image() -> None:
    """Test image analysis with Ollama."""
    client = OllamaChatClient(host="http://localhost:11434", model="gemma4:12b-it-qat", additional_properties=120.0)

    image_uri = create_sample_image()

    message = Message(
        role="user",
        contents=[
            Content.from_text(text="What's in this image?"),
            Content.from_uri(uri=image_uri, media_type="image/png"),
        ],
    )

    response = await client.get_response([message])
    print(f"Image Response: {response}")


async def main() -> None:
    print("=== Testing Ollama Multimodal ===")
    await test_image()


if __name__ == "__main__":
    asyncio.run(main())
