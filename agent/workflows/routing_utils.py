from agent.workflows.state import State


def is_in_tool_use(state: State):
    return (
        state.messages
        and hasattr(state.messages[-1], "tool_calls")
        and state.messages[-1].tool_calls
    )
