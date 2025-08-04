import subprocess
import os
import json
from typing import Dict
from langchain_core.tools import tool


@tool
def fetch_pull_request(pr_url: str) -> Dict:
    """Fetch top level pull request status and reviews"""
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
            env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")},
        )
        return json.loads(top_level_pr.stdout)
    except Exception as e:
        print(f"Unable to fetch pull request for {pr_url}: {e}")
