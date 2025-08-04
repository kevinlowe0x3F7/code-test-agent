from agent.workflows.state import WorkflowPhase
import time


PR_POLLING_WAIT_NODE = "pr_polling_wait"


def pr_polling_wait(_state):
    """Wait before checking PR status. In production this would be done through webhooks."""
    print("✋ Entered PR polling node. Waiting")
    time.sleep(15)
    return {"current_phase": WorkflowPhase.PR_VALIDATION}
