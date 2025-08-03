from agent.workflows.nodes.llm_test_generator import (
    LLM_TEST_GENERATOR_NODE,
    llm_test_generator,
)
from agent.workflows.nodes.tool_execution import TOOL_EXECUTION_NODE, tool_execution
from agent.workflows.routing import route_after_llm
from agent.workflows.state import State
from langgraph.graph import StateGraph, START, END

graph_builder = StateGraph(State)

graph_builder.add_node(LLM_TEST_GENERATOR_NODE, llm_test_generator)
graph_builder.add_node(TOOL_EXECUTION_NODE, tool_execution)

graph_builder.add_edge(START, LLM_TEST_GENERATOR_NODE)
graph_builder.add_conditional_edges(
    LLM_TEST_GENERATOR_NODE,
    route_after_llm,
    {TOOL_EXECUTION_NODE: TOOL_EXECUTION_NODE, END: END},
)
graph_builder.add_edge(TOOL_EXECUTION_NODE, LLM_TEST_GENERATOR_NODE)

graph = graph_builder.compile()
