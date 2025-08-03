from enum import Enum
from typing import Annotated, List, Dict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel


class WorkflowPhase(Enum):
    INITIAL = "initial"
    TEST_GENERATION = "test_generation"
    CODE_VALIDATION = "code_validation"
    PR_SUBMISSION = "pr_submission"
    ERROR = "error"
    COMPLETED = "completed"


def add_commit(existing_commits: List[Dict], new_commit: Dict) -> List[Dict]:
    """Reducer to append new commit to list"""
    return existing_commits + [new_commit]


class State(BaseModel):
    target_file_path: str
    test_file_path: str | None = None
    error_message: str | None = None
    code_validation_pytest_retry_attempts: int = 0
    branch_name: str | None = None
    pr_url: str | None = None
    commits: Annotated[List[Dict], add_commit] = []
    messages: Annotated[list[BaseMessage], add_messages]
    current_phase: WorkflowPhase = WorkflowPhase.INITIAL
