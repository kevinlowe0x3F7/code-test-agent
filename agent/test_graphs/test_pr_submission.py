from agent.workflows.nodes.pr_submission import PR_SUBMISSION_NODE, pr_submission
from agent.workflows.nodes.error_handler import ERROR_HANDLER_NODE, error_handler
from agent.workflows.routing import route_after_pr_submission
from agent.workflows.state import State, WorkflowPhase
from langgraph.graph import StateGraph, START, END

test_graph = StateGraph(State)

test_graph.add_node(PR_SUBMISSION_NODE, pr_submission)
test_graph.add_node(ERROR_HANDLER_NODE, error_handler)

test_graph.add_edge(START, PR_SUBMISSION_NODE)

test_graph.add_conditional_edges(
    PR_SUBMISSION_NODE,
    route_after_pr_submission,
    {
        ERROR_HANDLER_NODE: ERROR_HANDLER_NODE,
        END: END,
    },
)

test_graph.add_edge("error_handler", END)

graph = test_graph.compile()

test_state = {
    "target_file_path": "src/example.py",
    "test_file_path": "test/test_example.py",
    "current_phase": WorkflowPhase.PR_SUBMISSION,
    "code_validation_pytest_retry_attempts": 0,
    "messages": [],
}

result = graph.invoke(test_state)
print(f"Finished execution of testing pr_submission: {result}")
