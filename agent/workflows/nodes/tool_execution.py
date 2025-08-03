from langchain_core.messages.tool import ToolMessage
from agent.tools.file_reader import read_file
from agent.workflows.state import State

TOOL_EXECUTION_NODE = "tool_execution"


def tool_execution(state: State):
    last_message = state.messages[-1]
    tool_messages = []

    for tool_call in last_message.tool_calls:
        try:
            if tool_call["name"] == "read_file":
                result = read_file.invoke(tool_call["args"])

            print(f"Got result from tool call execution: {result}")
            tool_messages.append(
                ToolMessage(content=str(result), tool_call_id=tool_call["id"])
            )
        except Exception as e:
            tool_messages.append(
                ToolMessage(content=f"Error: {e}", tool_call_id=tool_call["id"])
            )

    return {"messages": tool_messages}
