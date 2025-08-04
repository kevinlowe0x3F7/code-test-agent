import time
from datetime import datetime, timezone
from langchain_core.messages.human import HumanMessage
from agent.prompts.pr_validation import PR_COMMENT_RESPONSE_PROMPT
from agent.tools.github.fetch_pull_request import fetch_pull_request
from agent.tools.github.fetch_pull_request_review_comments import (
    fetch_pull_request_review_comments,
)
from agent.tools.github.merge_pull_request import merge_pull_request
from agent.tools.registry import get_all_tools
from agent.workflows.state import State, WorkflowPhase
from agent.models.anthropic import anthropic_model

PR_VALIDATION_NODE = "pr_validation"


def pr_validation(state: State):
    llm_with_tools = anthropic_model.bind_tools(get_all_tools())

    if not state.pr_url:
        print("ERROR: Missing PR url in pr_validation")
        return {
            "current_phase": WorkflowPhase.ERROR,
            "error_message": "Missing PR url - cannot get PR info",
        }

    # check PR status
    pr_info = fetch_pull_request.invoke({"pr_url": state.pr_url})
    print(f"Top level PR: {pr_info}")
    if "state" not in pr_info or "mergeable" not in pr_info or "reviews" not in pr_info:
        print("ERROR: Missing PR info in pr_validation")
        return {
            "current_phase": WorkflowPhase.ERROR,
            "error_message": "Missing PR info, can't determine whether pr is done",
        }

    pr_status = pr_info["state"]
    if pr_status == "CLOSED":
        print("❌ PR was closed")
        return {"current_phase": WorkflowPhase.COMPLETED}
    mergeability = pr_info["mergeable"]
    reviews = pr_info["reviews"]
    # TODO in production this would probably just be handled by mergeability and GH approval rules
    has_approved = any(review["state"] == "APPROVED" for review in reviews)
    if mergeability == "MERGEABLE" and has_approved:
        print("🎉 Merging in PR")
        merge_pull_request.invoke({"pr_url": state.pr_url})
        return {"current_phase": WorkflowPhase.COMPLETED}

    last_processed_time = datetime.fromtimestamp(
        state.reviews_last_processed or 0, tz=timezone.utc
    )

    def is_unprocessed(review, ts_getter):
        ts = ts_getter(review)
        if ts is None:
            return False
        submitted_time = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
        return submitted_time > last_processed_time

    unprocessed_reviews = list(
        filter(
            lambda review: is_unprocessed(review, lambda r: r["submittedAt"]), reviews
        )
    )
    if len(unprocessed_reviews) == 0:
        print("⏳ No reviews to process, waiting")
        return {"current_phase": WorkflowPhase.PR_VALIDATION}

    # New comments, need to invoke LLM with a new message
    top_level_pr_review_comments = list(map(lambda r: r["body"], unprocessed_reviews))

    comments = fetch_pull_request_review_comments.invoke({"pr_url": state.pr_url})
    relevant_comments = [
        {
            "body": comment["body"],
            "path": comment["path"],
            "line": comment["line"],
            "diff_hunk": comment["diff_hunk"],
            "side": comment["side"],
            "start_line": comment["start_line"],
        }
        for comment in comments
        if is_unprocessed(comment, lambda c: c["created_at"])
    ]

    next_processed_time = int(time.time())
    human_message = HumanMessage(
        PR_COMMENT_RESPONSE_PROMPT.format(
            top_level_comments=top_level_pr_review_comments,
            line_comments=relevant_comments,
        )
    )
    print("💬 Sending message to LLM in PR validation")
    response = llm_with_tools.invoke(state.messages + [human_message])

    print(f"Got response in pr_validator with added prompts: {response}")
    return {
        "messages": [human_message, response],
        "current_phase": WorkflowPhase.PR_VALIDATION,
        "code_validation_pytest_retry_attempts": 0,
        "reviews_last_processed": next_processed_time,
    }
