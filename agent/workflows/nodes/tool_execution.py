from langchain_core.messages.tool import ToolMessage
from agent.tools.registry import get_tool_by_name
from agent.workflows.state import State

TOOL_EXECUTION_NODE = "tool_execution"


def tool_execution(state: State):
    last_message = state.messages[-1]
    tool_messages = []

    for tool_call in last_message.tool_calls:
        try:
            tool = get_tool_by_name(tool_call["name"])
            if tool:
                result = tool.invoke(tool_call["args"])
            else:
                result = f"Unknown tool: {tool_call['name']}"

            print(f"Got result from tool call execution: {result}")
            tool_messages.append(
                ToolMessage(content=str(result), tool_call_id=tool_call["id"])
            )
        except Exception as e:
            tool_messages.append(
                ToolMessage(content=f"Error: {e}", tool_call_id=tool_call["id"])
            )

    return {"messages": tool_messages}
