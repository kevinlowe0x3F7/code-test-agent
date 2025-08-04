from langchain_core.messages.tool import ToolMessage
from agent.tools.registry import get_tool_by_name
from agent.workflows.state import State, WorkflowPhase

TOOL_EXECUTION_NODE = "tool_execution"


def tool_execution(state: State):
    last_message = state.messages[-1]
    tool_messages = []
    state_updates = {}

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        try:
            tool = get_tool_by_name(tool_name)
            if tool:
                result = tool.invoke(tool_args)
            else:
                result = f"Unknown tool: {tool_name}"

            if tool_name == "write_file":
                if state.current_phase == WorkflowPhase.TEST_GENERATION and result:
                    state_updates["current_phase"] = (
                        WorkflowPhase.TEST_GENERATION_COMPLETED
                    )
                elif (
                    state.current_phase
                    == WorkflowPhase.PR_VALIDATION_ADDRESSING_COMMENTS
                ):
                    # This LLM wrote something to the file
                    state_updates["current_phase"] = (
                        WorkflowPhase.PR_VALIDATION_CHANGES_MADE
                    )
                    state_updates["code_validation_pytest_retry_attempts"] = 0

            print(f"Got result from tool call execution: {result}")
            tool_messages.append(
                ToolMessage(content=str(result), tool_call_id=tool_call["id"])
            )
        except Exception as e:
            tool_messages.append(
                ToolMessage(content=f"Error: {e}", tool_call_id=tool_call["id"])
            )

    return {"messages": tool_messages, **state_updates}
