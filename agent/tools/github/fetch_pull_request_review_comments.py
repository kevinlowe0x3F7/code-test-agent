import subprocess
import os
import json
from typing import Dict
from langchain_core.tools import tool


@tool
def fetch_pull_request_review_comments(pr_url: str) -> Dict:
    """Fetch review comments"""
    bot_env = os.environ.copy()
    bot_env["GITHUB_TOKEN"] = os.getenv("GITHUB_TOKEN")
    pr_number = pr_url.split("/")[-1]
    repo_path = "/".join(pr_url.split("/")[-4:-2])
    try:
        review_comments = subprocess.run(
            [
                "gh",
                "api",
                "-H",
                "Accept: application/vnd.github+json",
                "-H",
                "X-GitHub-Api-Version: 2022-11-28",
                f"/repos/{repo_path}/pulls/{pr_number}/comments",
            ],
            capture_output=True,
            text=True,
            env=bot_env,
        )
        return json.loads(review_comments.stdout)
    except Exception as e:
        print(f"Unable to fetch pull request review comments for {pr_url}: {e}")
