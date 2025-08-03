from langchain_core.tools import tool
import subprocess


@tool
def push_branch(branch_name: str, work_dir: str = "."):
    """Push branch to upstream remote"""
    subprocess.run(
        ["git", "push", "-u", "origin", branch_name],
        cwd=work_dir,
        capture_output=True,
        text=True,
    )
    return {
        "success": True,
    }
