from typing import Annotated
from langgraph.graph.message import add_messages
from pydantic import BaseModel


class State(BaseModel):
    target_file_path: str
    messages: Annotated[list[str], add_messages]
