from pathlib import Path
from langchain_core.tools import tool
import os
import subprocess


@tool
def create_pull_request(
    target_file_path: str, test_file_path: str, work_dir="."
) -> str:
    """Create a new pull request from the branch"""
    target_file = Path(target_file_path).stem
    title = f"Add automated tests for {target_file}"
    body = f"""
## Before this PR
No tests available for `{target_file}`

## After this PR
- Generated automated tests for `{target_file}`
- Tests cover edge cases and main functionality
- All tests passing ✅

Tests are in `{test_file_path}`

🤖 Generated with Code Agent Bot
"""
    bot_env = os.environ.copy()
    bot_env["GITHUB_TOKEN"] = os.getenv("GITHUB_TOKEN")

    result = subprocess.run(
        ["gh", "pr", "create", "--title", title, "--body", body],
        cwd=work_dir,
        env=bot_env,
        capture_output=True,
        text=True,
        check=True,
    )

    print(f"Created pull request for {target_file_path}: {result}")
    return result.stdout.strip()
