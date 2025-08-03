from .file_reader import read_file
from .file_writer import write_file

TOOL_REGISTRY = {
    "read_file": read_file,
    "write_file": write_file,
}


def get_all_tools():
    """For binding to LLM"""
    return list(TOOL_REGISTRY.values())


def get_tool_by_name(name: str):
    """For tool execution"""
    return TOOL_REGISTRY.get(name)
