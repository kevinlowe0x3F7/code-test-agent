from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from agent.prompts.test_generation import SYSTEM_PROMPT, TEST_GENERATION_PROMPT
from agent.tools.registry import get_all_tools
from agent.workflows.state import State, WorkflowPhase
from agent.models.anthropic import anthropic_model
from pathlib import Path

LLM_TEST_GENERATOR_NODE = "llm_test_generator"


def llm_test_generator(state: State):
    llm_with_tools = anthropic_model.bind_tools(get_all_tools())

    file_path = state.target_file_path
    if state.current_phase != WorkflowPhase.TEST_GENERATION:
        test_file_path = _generate_test_file_path(file_path)

        # First time this node is running, add prompts
        messages = state.messages + [
            SystemMessage(SYSTEM_PROMPT),
            HumanMessage(
                TEST_GENERATION_PROMPT.format(
                    file_path=file_path, test_file_path=test_file_path
                )
            ),
        ]

        response = llm_with_tools.invoke(messages)

        print(f"Got response in llm_test_generator with added prompts: {response}")
        return {
            "messages": [*messages, response],
            "current_phase": WorkflowPhase.TEST_GENERATION,
            "test_file_path": test_file_path,
        }
    else:
        # We're in tool loop - continue conversation
        response = llm_with_tools.invoke(state.messages)

        print(f"Got response in llm_test_generator in tool loop: {response}")
        return {"messages": [response], "current_phase": WorkflowPhase.TEST_GENERATION}


def _generate_test_file_path(source_file_path: str) -> str:
    """Generate test file path following pytest conventions."""
    source_path = Path(source_file_path)

    # Convert src/example.py -> test/test_example.py
    if source_path.parts[0] == "src":
        # Remove 'src' prefix and add 'test' prefix with 'test_' filename
        relative_path = Path(*source_path.parts[1:])
        test_filename = f"test_{relative_path.stem}.py"
        test_path = Path("test") / relative_path.parent / test_filename
    else:
        # Default: same directory with test_ prefix
        test_filename = f"test_{source_path.stem}.py"
        test_path = source_path.parent / test_filename

    return str(test_path)
