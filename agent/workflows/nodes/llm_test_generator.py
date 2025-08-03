from langchain_core.messages.human import HumanMessage
from agent.workflows.state import State
from agent.models.anthropic import anthropic_model

LLM_TEST_GENERATOR_NODE = "llm_test_generator"


def llm_test_generator(state: State):
    file_path = state.target_file_path
    response = anthropic_model.invoke(
        [HumanMessage(content="Repeat after me: " + file_path)]
    )
    print(f"Generating test for {file_path} with response: {response}")
    return state
