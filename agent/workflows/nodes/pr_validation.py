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
    if not state.pr_url:
        print("ERROR: Missing PR url in pr_validation")
        return {
            "current_phase": WorkflowPhase.ERROR,
            "error_message": "Missing PR url - cannot get PR info",
        }

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

    reviews = pr_info["reviews"]

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

    # New comments, need to invoke LLM with a new message
    top_level_pr_review_comments = list(map(lambda r: r["body"], unprocessed_reviews))

    comments = fetch_pull_request_review_comments.invoke({"pr_url": state.pr_url})
    relevant_comments = [
        {
            "body": comment["body"],
            "path": comment["path"],
            "line": comment["line"],
            "side": comment["side"],
            "start_line": comment["start_line"],
        }
        for comment in comments
        if is_unprocessed(comment, lambda c: c["created_at"])
    ]

    has_comments = len(top_level_pr_review_comments) > 0 or len(relevant_comments) > 0

    human_message = HumanMessage(
        PR_COMMENT_RESPONSE_PROMPT.format(
            top_level_comments=top_level_pr_review_comments,
            line_comments=relevant_comments,
            test_file_path=state.test_file_path,
        )
    )

    if (
        has_comments
        and state.current_phase != WorkflowPhase.PR_VALIDATION_ADDRESSING_COMMENTS
    ):
        llm_with_tools = anthropic_model.bind_tools(get_all_tools())
        print("💬 Sending message to LLM in PR validation")
        response = llm_with_tools.invoke(state.messages + [human_message])

        print(f"Got response in pr_validator with added prompts: {response}")
        return {
            "messages": [human_message, response],
            "current_phase": WorkflowPhase.PR_VALIDATION_ADDRESSING_COMMENTS,
            "reviews_last_processed": int(time.time()),
        }

    if state.current_phase == WorkflowPhase.PR_VALIDATION_ADDRESSING_COMMENTS:
        # We're in tool loop - continue conversation
        llm_with_tools = anthropic_model.bind_tools(get_all_tools())
        print("🔄 Tool use loop in PR validation")
        response = llm_with_tools.invoke(state.messages)

        print(f"Got response in pr_validation in tool loop: {response}")
        return {
            "messages": [response],
            "current_phase": WorkflowPhase.PR_VALIDATION_ADDRESSING_COMMENTS,
        }

    # TODO in production this would probably just be handled by mergeability and GH approval rules
    mergeability = pr_info["mergeable"]
    has_approved = any(review["state"] == "APPROVED" for review in reviews)
    if mergeability == "MERGEABLE" and has_approved:
        print("🎉 Merging in PR")
        merge_pull_request.invoke({"pr_url": state.pr_url})
        return {"current_phase": WorkflowPhase.COMPLETED}

    print("⏳ No reviews to process, waiting")
    return {"current_phase": WorkflowPhase.PR_VALIDATION_WAITING}
