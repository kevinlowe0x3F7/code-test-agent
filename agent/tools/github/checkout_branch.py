from langchain_core.tools import tool
import subprocess


@tool
def checkout_git_branch(branch_name: str, work_dir: str = ".") -> str:
    """Checkout branch"""
    subprocess.run(
        ["git", "checkout", branch_name],
        cwd=work_dir,
        capture_output=True,
        text=True,
    )
    return branch_name
