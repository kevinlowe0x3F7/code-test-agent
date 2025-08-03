from agent.workflows.nodes.code_validation import CODE_VALIDATION_NODE
from agent.workflows.nodes.error_handler import ERROR_HANDLER_NODE
from agent.workflows.nodes.pr_submission import PR_SUBMISSION_NODE
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
    print(
        f"WARNING: Unexpected state after test_generation {state.current_phase}, ending workflow"
    )
    return END


def route_after_tool_execution(state: State):
    """Route after tool execution - depends on which phase we're in"""
    if state.current_phase == WorkflowPhase.ERROR:
        return ERROR_HANDLER_NODE

    if state.current_phase == WorkflowPhase.TEST_GENERATION:
        return TEST_GENERATION_NODE
    if state.current_phase == WorkflowPhase.CODE_VALIDATION:
        return CODE_VALIDATION_NODE

    print(
        f"WARNING: Unexpected state after tool_execution {state.current_phase}, ending workflow"
    )
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
    elif state.current_phase == WorkflowPhase.CODE_VALIDATION:
        return PR_SUBMISSION_NODE

    print(
        f"WARNING: Unexpected state after code_validation {state.current_phase}, ending workflow"
    )
    return END


def route_after_pr_submission(state: State):
    """Route after code validation node"""
    if state.current_phase == WorkflowPhase.ERROR:
        return ERROR_HANDLER_NODE
    elif state.current_phase == WorkflowPhase.PR_SUBMISSION:
        return END

    print(
        f"WARNING: Unexpected state after code_validation {state.current_phase}, ending workflow"
    )
    return END
