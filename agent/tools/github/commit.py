from langchain_core.tools import tool
import subprocess
import time
from pathlib import Path


@tool
def commit_test_file(
    target_file_path: str, test_file_path: str, work_dir: str = "."
) -> str:
    """Commit test file to local git"""
    filename = Path(target_file_path).stem
    commit_message = f"Add automated tests for {filename}"

    # TODO edge case of if there was nothing to add?
    subprocess.run(["git", "add", test_file_path], cwd=work_dir, check=True)

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            commit_message,
            "--author",
            "Code Test Agent <codeagentbot@gmail.com>",
        ],
        cwd=work_dir,
        capture_output=True,
        text=True,
        check=True,
    )

    # Get commit hash
    hash_result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=work_dir,
        capture_output=True,
        text=True,
        check=True,
    )

    commit_hash = hash_result.stdout.strip()

    return {
        "hash": commit_hash,
        "message": commit_message,
        "timestamp": int(time.time()),
    }
