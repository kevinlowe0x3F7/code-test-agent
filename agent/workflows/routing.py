from agent.workflows.nodes.code_validation import CODE_VALIDATION_NODE
from agent.workflows.nodes.error_handler import ERROR_HANDLER_NODE
from agent.workflows.nodes.pr_polling_wait import PR_POLLING_WAIT_NODE
from agent.workflows.nodes.pr_submission import PR_SUBMISSION_NODE
from agent.workflows.nodes.pr_validation import PR_VALIDATION_NODE
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
    elif state.current_phase == WorkflowPhase.TEST_GENERATION_COMPLETED:
        return CODE_VALIDATION_NODE

    return TEST_GENERATION_NODE


def route_after_tool_execution(state: State):
    """Route after tool execution - depends on which phase we're in"""
    if state.current_phase == WorkflowPhase.ERROR:
        return ERROR_HANDLER_NODE

    if state.current_phase == WorkflowPhase.TEST_GENERATION:
        return TEST_GENERATION_NODE
    elif state.current_phase == WorkflowPhase.CODE_VALIDATION:
        return CODE_VALIDATION_NODE
    elif (
        state.current_phase == WorkflowPhase.PR_VALIDATION
        or state.current_phase == WorkflowPhase.PR_VALIDATION_ADDRESSING_COMMENTS
    ):
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
    elif state.current_phase == WorkflowPhase.CODE_VALIDATION_COMPLETED:
        return PR_SUBMISSION_NODE

    print(
        f"WARNING: Unexpected state after code_validation {state.current_phase}, ending workflow"
    )
    return END


def route_after_pr_submission(state: State):
    """Route after pr submission node"""
    if state.current_phase == WorkflowPhase.ERROR:
        return ERROR_HANDLER_NODE
    elif state.current_phase == WorkflowPhase.PR_SUBMISSION:
        # Give time for PR to be created
        return PR_POLLING_WAIT_NODE

    print(
        f"WARNING: Unexpected state after code_validation {state.current_phase}, ending workflow"
    )
    return END


def route_after_pr_validation(state: State):
    """Route after pr validation node"""
    if state.current_phase == WorkflowPhase.ERROR:
        return ERROR_HANDLER_NODE
    elif (
        state.messages
        and hasattr(state.messages[-1], "tool_calls")
        and state.messages[-1].tool_calls
    ):
        return TOOL_EXECUTION_NODE
    elif state.current_phase == WorkflowPhase.PR_VALIDATION_CHANGES_MADE:
        return CODE_VALIDATION_NODE
    elif state.current_phase == WorkflowPhase.COMPLETED:
        return END
    elif state.current_phase == WorkflowPhase.PR_VALIDATION_WAITING:
        return PR_POLLING_WAIT_NODE

    return PR_VALIDATION_NODE


def route_after_pr_polling_wait(_state):
    """Route after pr polling, always go back to pr validation"""
    return PR_VALIDATION_NODE
