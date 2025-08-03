from langchain_core.tools import tool


def _read_file_impl(file_path: str) -> str:
    """Pure Python implementation"""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return f"Error reading file {file_path}: {e}"


@tool
def read_file(file_path: str) -> str:
    """Read and return contents of a file for analysis."""
    return _read_file_impl(file_path)
