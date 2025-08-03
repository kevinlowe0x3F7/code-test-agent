import os
import subprocess
from langchain_core.messages.human import HumanMessage
from agent.prompts.code_validation import CODE_VALIDATION_PROMPT
from agent.tools.registry import get_all_tools
from agent.workflows.state import State, WorkflowPhase
from agent.models.anthropic import anthropic_model

CODE_VALIDATION_NODE = "code_validation"


def code_validation(state: State):
    llm_with_tools = anthropic_model.bind_tools(get_all_tools())

    if not state.test_file_path:
        print("ERROR: Missing test_file_path in code_validation")
        return {
            "current_phase": WorkflowPhase.ERROR,
            "error_message": "Missing test_file_path - cannot validate tests",
        }
    elif not os.path.exists(state.test_file_path):
        print("ERROR: Missing test file in code_validation")
        return {
            "current_phase": WorkflowPhase.ERROR,
            "error_message": "Test file not found - cannot validate tests",
        }
    elif state.code_validation_pytest_retry_attempts >= 3:
        return {
            "current_phase": WorkflowPhase.ERROR,
            "error_message": "Unable to fix the test file during test validation",
        }

    pytest_result = _run_pytest(state.test_file_path)
    print(f"Got pytest result: {pytest_result}")

    if pytest_result["passed"]:
        return {"current_phase": WorkflowPhase.COMPLETED}

    pytest_output = pytest_result.get("raw_stdout", "") + pytest_result.get(
        "raw_stderr", ""
    )
    human_message = HumanMessage(
        CODE_VALIDATION_PROMPT.format(
            test_file_path=state.test_file_path, pytest_result=pytest_output
        )
    )
    if state.current_phase != WorkflowPhase.CODE_VALIDATION:
        response = llm_with_tools.invoke(state.messages + [human_message])

        print(f"Got response in code_validator with added prompts: {response}")
        return {
            "messages": [human_message, response],
            "current_phase": WorkflowPhase.CODE_VALIDATION,
            "code_validation_pytest_retry_attempts": state.code_validation_pytest_retry_attempts
            + 1,
        }
    else:
        # We're in tool loop - continue conversation
        response = llm_with_tools.invoke(state.messages + [human_message])

        print(f"Got response in code_validator in tool loop: {response}")
        return {
            "messages": [response],
            "code_validation_pytest_retry_attempts": state.code_validation_pytest_retry_attempts
            + 1,
        }


def _run_pytest(test_file_path: str) -> dict:
    """Run pytest with minimal assumptions about output format"""
    try:
        result = subprocess.run(
            ["pytest", test_file_path, "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        return {
            "return_code": result.returncode,
            "passed": result.returncode == 0,  # Only rely on return code
            "raw_stdout": result.stdout,
            "raw_stderr": result.stderr,
        }
    except Exception as e:
        return {"passed": False, "error": str(e)}
