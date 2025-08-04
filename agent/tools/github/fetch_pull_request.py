import subprocess
import os
import json
from typing import Dict
from langchain_core.tools import tool


@tool
def fetch_pull_request(pr_url: str) -> Dict:
    """Fetch top level pull request status and reviews"""
    bot_env = os.environ.copy()
    bot_env["GITHUB_TOKEN"] = os.getenv("GITHUB_TOKEN")
    try:
        # Top level PR has state and top level comments + top level review comments
        top_level_pr = subprocess.run(
            [
                "gh",
                "pr",
                "view",
                pr_url,
                "--comments",
                "--json",
                "comments,reviews,state,mergeable,mergeStateStatus",
            ],
            capture_output=True,
            text=True,
            env=bot_env,
        )
        return json.loads(top_level_pr.stdout)
    except Exception as e:
        print(f"Unable to fetch pull request for {pr_url}: {e}")
