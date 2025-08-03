import time
from pathlib import Path
from langchain_core.tools import tool
import subprocess


@tool
def create_git_branch(target_file_path: str, work_dir: str = ".") -> str:
    """Create new branch based off of target_file_path name"""
    filename = Path(target_file_path).stem
    timestamp = int(time.time())
    branch_name = f"agent-test-{filename}-{timestamp}"

    subprocess.run(
        ["git", "checkout", "-b", branch_name],
        cwd=work_dir,
        capture_output=True,
        text=True,
    )
    return branch_name
