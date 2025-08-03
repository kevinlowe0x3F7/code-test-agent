from agent.workflows.state import State

LLM_TEST_GENERATOR_NODE = "llm_test_generator"


def llm_test_generator(state: State):
    file_path = state.target_file_path
    print(f"Generating test for {file_path}")
    return state
