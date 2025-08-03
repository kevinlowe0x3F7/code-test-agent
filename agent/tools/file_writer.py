import os
from langchain_core.tools import tool


def _write_file_impl(file_path: str, content: str) -> str:
    """Pure Python implementation for writing files."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as f:
            f.write(content)
        return f"Successfully wrote file: {file_path}"
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")
        return f"Error writing file {file_path}: {e}"


@tool
def write_file(file_path: str, content: str) -> str:
    """Write content to specified file path."""
    return _write_file_impl(file_path, content)
