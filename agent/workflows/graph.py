from agent.workflows.nodes.llm_test_generator import (
    LLM_TEST_GENERATOR_NODE,
    llm_test_generator,
)
from agent.workflows.nodes.tool_execution import TOOL_EXECUTION_NODE, tool_execution
from agent.workflows.nodes.code_validation import CODE_VALIDATION_NODE, code_validation
from agent.workflows.nodes.error_handler import ERROR_HANDLER_NODE, error_handler
from agent.workflows.routing import (
    route_after_llm_test_generator,
    route_after_tool_execution,
    route_after_code_validation,
)
from agent.workflows.state import State
from langgraph.graph import StateGraph, START, END

graph_builder = StateGraph(State)

graph_builder.add_node(LLM_TEST_GENERATOR_NODE, llm_test_generator)
graph_builder.add_node(TOOL_EXECUTION_NODE, tool_execution)
graph_builder.add_node(CODE_VALIDATION_NODE, code_validation)
graph_builder.add_node(ERROR_HANDLER_NODE, error_handler)

graph_builder.add_edge(START, LLM_TEST_GENERATOR_NODE)

graph_builder.add_conditional_edges(
    LLM_TEST_GENERATOR_NODE,
    route_after_llm_test_generator,
    {
        TOOL_EXECUTION_NODE: TOOL_EXECUTION_NODE,
        CODE_VALIDATION_NODE: CODE_VALIDATION_NODE,
        ERROR_HANDLER_NODE: ERROR_HANDLER_NODE,
        END: END,
    },
)

graph_builder.add_conditional_edges(
    TOOL_EXECUTION_NODE,
    route_after_tool_execution,
    {
        LLM_TEST_GENERATOR_NODE: LLM_TEST_GENERATOR_NODE,
        CODE_VALIDATION_NODE: CODE_VALIDATION_NODE,
        ERROR_HANDLER_NODE: ERROR_HANDLER_NODE,
        END: END,
    },
)

graph_builder.add_conditional_edges(
    CODE_VALIDATION_NODE,
    route_after_code_validation,
    {
        ERROR_HANDLER_NODE: ERROR_HANDLER_NODE,
        TOOL_EXECUTION_NODE: TOOL_EXECUTION_NODE,
        END: END,
    },
)

graph_builder.add_edge(ERROR_HANDLER_NODE, END)

graph = graph_builder.compile()
