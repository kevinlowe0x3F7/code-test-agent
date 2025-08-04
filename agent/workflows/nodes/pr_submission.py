import os
from agent.tools.github.commit import commit_test_file
from agent.tools.github.create_branch import create_git_branch
from agent.tools.github.create_pull_request import create_pull_request
from agent.tools.github.push_branch import push_branch
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

    # TODO: fetch latest main branch in production
    # TODO: make sure we're on main branch
    try:
        branch_name = (
            state.branch_name
            if state.branch_name
            else create_git_branch.invoke({"target_file_path": state.target_file_path})
        )
        commit_info = commit_test_file.invoke(
            {
                "test_file_path": state.test_file_path,
                "target_file_path": state.target_file_path,
            }
        )
        push_branch.invoke({"branch_name": branch_name})

        pr_url = (
            state.pr_url
            if state.pr_url
            else create_pull_request.invoke(
                {
                    "test_file_path": state.test_file_path,
                    "target_file_path": state.target_file_path,
                }
            )
        )

        return {
            "current_phase": WorkflowPhase.PR_SUBMISSION,
            "branch_name": branch_name,
            "commits": commit_info,
            "pr_url": pr_url,
        }

    except Exception as e:
        print(f"Error running through github workflow: {str(e)}")
        return {
            "current_phase": WorkflowPhase.ERROR,
            "error_message": str(e),
        }
