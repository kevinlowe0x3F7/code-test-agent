from enum import Enum
from typing import Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel


class WorkflowPhase(Enum):
    INITIAL = "initial"
    TEST_GENERATION = "test_generation"
    COMPLETED = "completed"


class State(BaseModel):
    target_file_path: str
    test_file_path: str | None = None
    messages: Annotated[list[BaseMessage], add_messages]
    current_phase: WorkflowPhase = WorkflowPhase.INITIAL
