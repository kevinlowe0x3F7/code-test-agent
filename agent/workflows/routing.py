from agent.workflows.nodes.tool_execution import TOOL_EXECUTION_NODE
from agent.workflows.state import State
from langgraph.graph import END


def route_after_llm(state: State):
    last_message = state.messages[-1]
    if last_message.tool_calls:
        return TOOL_EXECUTION_NODE
    else:
        return END
