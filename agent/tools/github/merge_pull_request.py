import subprocess
import os
from langchain_core.tools import tool


@tool
def merge_pull_request(pr_url: str):
    """Merge pull request"""
    try:
        subprocess.run(
            [
                "gh",
                "pr",
                "merge",
                pr_url,
                "-s",  # Squash
                "-d",  # Delete branch after merge
            ],
            capture_output=True,
            text=True,
            env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")},
        )
    except Exception as e:
        print(f"Unable to fetch pull request for {pr_url}: {e}")
