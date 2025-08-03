from agent.workflows.nodes.llm_test_generator import (
    LLM_TEST_GENERATOR_NODE,
    llm_test_generator,
)
from agent.workflows.state import State
from langgraph.graph import StateGraph, START, END

graph_builder = StateGraph(State)

graph_builder.add_node(LLM_TEST_GENERATOR_NODE, llm_test_generator)
graph_builder.add_edge(START, LLM_TEST_GENERATOR_NODE)
graph_builder.add_edge(LLM_TEST_GENERATOR_NODE, END)

graph = graph_builder.compile()
