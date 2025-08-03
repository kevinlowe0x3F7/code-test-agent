from langchain_core.messages.human import HumanMessage
from agent.prompts.test_generation import TEST_GENERATION_PROMPT
from agent.tools.file_reader import read_file
from agent.workflows.state import State, WorkflowPhase
from agent.models.anthropic import anthropic_model

LLM_TEST_GENERATOR_NODE = "llm_test_generator"


def llm_test_generator(state: State):
    llm_with_tools = anthropic_model.bind_tools([read_file])

    file_path = state.target_file_path
    if state.current_phase != WorkflowPhase.TEST_GENERATION:
        # First time this node is running, add prompts
        human_message = HumanMessage(TEST_GENERATION_PROMPT.format(file_path=file_path))
        # messages = state.messages + [SystemMessage(SYSTEM_PROMPT), human_message]
        messages = [human_message]

        response = llm_with_tools.invoke(messages)

        return {
            "messages": [*messages, response],
            "current_phase": WorkflowPhase.TEST_GENERATION,
        }
    else:
        # We're in tool loop - continue conversation
        response = llm_with_tools.invoke(state.messages)

        return {"messages": [response], "current_phase": WorkflowPhase.TEST_GENERATION}
