from agent.workflows.state import State, WorkflowPhase

ERROR_HANDLER_NODE = "error_handler"


def error_handler(state: State):
    print(f"Workflow failed: {state.error_message or 'Unknown error'}")
    return {"current_phase": WorkflowPhase.ERROR}
