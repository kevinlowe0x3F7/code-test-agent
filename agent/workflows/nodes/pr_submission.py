import os
from agent.workflows.state import State, WorkflowPhase

PR_SUBMISSION_NODE = "pr_submission"


def pr_submission(state: State):
    if not state.test_file_path:
        print("ERROR: Missing test_file_path in pr_submission")
        return {
            "current_phase": WorkflowPhase.ERROR,
            "error_message": "Missing test_file_path - cannot push to Github",
        }
    elif not os.path.exists(state.test_file_path):
        print("ERROR: Missing test file in pr_submission")
        return {
            "current_phase": WorkflowPhase.ERROR,
            "error_message": "Test file not found - cannot push to Github",
        }

    # fetch latest develop
    # create branch (decide naming convention)
    # add test file to commit
    # commit (decide commit message template)
    # push branch to remote
    # create PR (decide PR template)
    return {"current_phase": WorkflowPhase.PR_SUBMISSION}
