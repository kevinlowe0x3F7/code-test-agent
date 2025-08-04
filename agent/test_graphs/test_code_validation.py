from agent.workflows.nodes.code_validation import code_validation
from agent.workflows.nodes.pr_submission import PR_SUBMISSION_NODE, pr_submission
from agent.workflows.nodes.tool_execution import tool_execution
from agent.workflows.nodes.error_handler import error_handler
from agent.workflows.routing import route_after_code_validation
from agent.workflows.state import State, WorkflowPhase
from langgraph.graph import StateGraph, START, END

test_graph = StateGraph(State)

test_graph.add_node("code_validation", code_validation)
test_graph.add_node("tool_execution", tool_execution)
test_graph.add_node("error_handler", error_handler)
test_graph.add_node(PR_SUBMISSION_NODE, pr_submission)

test_graph.add_edge(START, "code_validation")

test_graph.add_conditional_edges(
    "code_validation",
    route_after_code_validation,
    {
        "error_handler": "error_handler",
        "tool_execution": "tool_execution",
        PR_SUBMISSION_NODE: PR_SUBMISSION_NODE,
        END: END,
    },
)

test_graph.add_edge("tool_execution", "code_validation")
test_graph.add_edge("error_handler", END)

graph = test_graph.compile()

test_state = {
    "target_file_path": "src/example.py",
    "test_file_path": "test/test_example.py",
    "current_phase": WorkflowPhase.INITIAL,  # Will trigger first-time logic
    "code_validation_pytest_retry_attempts": 0,
    "messages": [],
}

result = graph.invoke(test_state)
