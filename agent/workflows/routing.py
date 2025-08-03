from agent.workflows.nodes.code_validation import CODE_VALIDATION_NODE
from agent.workflows.nodes.error_handler import ERROR_HANDLER_NODE
from agent.workflows.nodes.tool_execution import TOOL_EXECUTION_NODE
from agent.workflows.nodes.test_generation import TEST_GENERATION_NODE
from agent.workflows.state import State, WorkflowPhase
from langgraph.graph import END


def route_after_test_generation(state: State):
    """Route after test generation node"""
    if state.current_phase == WorkflowPhase.ERROR:
        return ERROR_HANDLER_NODE
    elif (
        state.messages
        and hasattr(state.messages[-1], "tool_calls")
        and state.messages[-1].tool_calls
    ):
        return TOOL_EXECUTION_NODE

    # If test generation is done, move to code validation
    if state.current_phase == WorkflowPhase.TEST_GENERATION:
        return CODE_VALIDATION_NODE

    # Default fallback
    return END


def route_after_tool_execution(state: State):
    """Route after tool execution - depends on which phase we're in"""
    if state.current_phase == WorkflowPhase.ERROR:
        return ERROR_HANDLER_NODE

    if state.current_phase == WorkflowPhase.TEST_GENERATION:
        return TEST_GENERATION_NODE
    if state.current_phase == WorkflowPhase.CODE_VALIDATION:
        return CODE_VALIDATION_NODE

    return END


def route_after_code_validation(state: State):
    """Route after code validation node"""
    if state.current_phase == WorkflowPhase.ERROR:
        return ERROR_HANDLER_NODE
    elif (
        state.messages
        and hasattr(state.messages[-1], "tool_calls")
        and state.messages[-1].tool_calls
    ):
        return TOOL_EXECUTION_NODE
    else:
        return END
