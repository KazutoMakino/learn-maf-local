# Copyright (c) Microsoft. All rights reserved.

"""Launch DevUI with folder discovery for the samples in this directory.

This sample demonstrates:
- Starting DevUI in directory discovery mode for this folder
- Auto-discovering agent/workflow entities defined in subfolders
"""

from pathlib import Path

from agent_framework.devui import serve


def main() -> None:
    """Launch DevUI with folder discovery."""
    samples_dir = Path(__file__).resolve().parent

    # Start DevUI and discover entities from this directory.
    serve(entities_dir=str(samples_dir), auto_open=True)


if __name__ == "__main__":
    main()

# Sample output:
# Starting Agent Framework DevUI on 127.0.0.1:8080
