from agent.workflows.state import WorkflowPhase
import time


PR_POLLING_WAIT_NODE = "pr_polling_wait"


def pr_polling_wait():
    """Wait before checking PR status. In production this would be done through webhooks."""
    time.sleep(30)
    return {"current_phase": WorkflowPhase.PR_VALIDATION}
