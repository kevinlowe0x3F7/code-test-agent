from agent.workflows.nodes.pr_polling_wait import PR_POLLING_WAIT_NODE, pr_polling_wait
from agent.workflows.nodes.pr_validation import PR_VALIDATION_NODE, pr_validation
from agent.workflows.nodes.test_generation import (
    TEST_GENERATION_NODE,
    test_generation,
)
from agent.workflows.nodes.tool_execution import TOOL_EXECUTION_NODE, tool_execution
from agent.workflows.nodes.code_validation import CODE_VALIDATION_NODE, code_validation
from agent.workflows.nodes.error_handler import ERROR_HANDLER_NODE, error_handler
from agent.workflows.nodes.pr_submission import PR_SUBMISSION_NODE, pr_submission
from agent.workflows.routing import (
    route_after_pr_polling_wait,
    route_after_pr_submission,
    route_after_pr_validation,
    route_after_test_generation,
    route_after_tool_execution,
    route_after_code_validation,
)
from agent.workflows.state import State
from langgraph.graph import StateGraph, START, END

graph_builder = StateGraph(State)

graph_builder.add_node(TEST_GENERATION_NODE, test_generation)
graph_builder.add_node(TOOL_EXECUTION_NODE, tool_execution)
graph_builder.add_node(CODE_VALIDATION_NODE, code_validation)
graph_builder.add_node(ERROR_HANDLER_NODE, error_handler)
graph_builder.add_node(PR_SUBMISSION_NODE, pr_submission)
graph_builder.add_node(PR_VALIDATION_NODE, pr_validation)
graph_builder.add_node(PR_POLLING_WAIT_NODE, pr_polling_wait)

graph_builder.add_edge(START, TEST_GENERATION_NODE)

graph_builder.add_conditional_edges(
    TEST_GENERATION_NODE,
    route_after_test_generation,
    {
        TOOL_EXECUTION_NODE: TOOL_EXECUTION_NODE,
        CODE_VALIDATION_NODE: CODE_VALIDATION_NODE,
        ERROR_HANDLER_NODE: ERROR_HANDLER_NODE,
        END: END,
    },
)

graph_builder.add_conditional_edges(
    CODE_VALIDATION_NODE,
    route_after_code_validation,
    {
        TOOL_EXECUTION_NODE: TOOL_EXECUTION_NODE,
        PR_SUBMISSION_NODE: PR_SUBMISSION_NODE,
        ERROR_HANDLER_NODE: ERROR_HANDLER_NODE,
        END: END,
    },
)

graph_builder.add_conditional_edges(
    TOOL_EXECUTION_NODE,
    route_after_tool_execution,
    {
        TEST_GENERATION_NODE: TEST_GENERATION_NODE,
        CODE_VALIDATION_NODE: CODE_VALIDATION_NODE,
        ERROR_HANDLER_NODE: ERROR_HANDLER_NODE,
        END: END,
    },
)

graph_builder.add_conditional_edges(
    PR_SUBMISSION_NODE,
    route_after_pr_submission,
    {
        PR_VALIDATION_NODE: PR_VALIDATION_NODE,
        ERROR_HANDLER_NODE: ERROR_HANDLER_NODE,
        END: END,
    },
)

graph_builder.add_conditional_edges(
    PR_VALIDATION_NODE,
    route_after_pr_validation,
    {
        TOOL_EXECUTION_NODE: TOOL_EXECUTION_NODE,
        PR_POLLING_WAIT_NODE: PR_POLLING_WAIT_NODE,
        ERROR_HANDLER_NODE: ERROR_HANDLER_NODE,
        END: END,
    },
)

graph_builder.add_conditional_edges(
    PR_POLLING_WAIT_NODE,
    route_after_pr_polling_wait,
    {PR_VALIDATION_NODE: PR_VALIDATION_NODE},
)

graph_builder.add_edge(ERROR_HANDLER_NODE, END)

graph = graph_builder.compile()
