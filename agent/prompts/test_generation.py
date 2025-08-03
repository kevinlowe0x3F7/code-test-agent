SYSTEM_PROMPT = """You are a Python test generator. Analyze the provided code and generate comprehensive unit tests."""

TEST_GENERATION_PROMPT = """
Analyze this Python file and generate pytest unit tests:

File: {file_path}
Test File: {test_file_path}

Requirements:
- Use pytest framework
- Test all public functions
- Include edge cases
- The test file should be ready to run pytest on it

First read the source file to understand the code, then generate comprehensive tests and write them to {test_file_path} using the write_file tool.
"""

"""
TODO for later, for better test generation

Advanced Prompt Engineering Elements:

  1. Example-driven Learning:
  - Provide exemplary test files as context: "Here are examples of well-written tests from this codebase..."
  - Show patterns: parametrized tests, fixtures, proper mocking
  - Demonstrate edge case coverage

  2. Regression-focused Rules:
  - Test boundary conditions (min/max values, empty inputs, None)
  - Test error paths and exception scenarios
  - Cover all code branches and decision points
  - Test integration points between modules
  - Validate state changes and side effects

  3. Mock Quality Guidelines:
  - Use realistic mock data that reflects production scenarios
  - Mock external dependencies (APIs, databases, file systems)
  - Ensure mocked responses cover success/failure cases
  - Validate mock interactions (call counts, arguments)

  4. Style & Structure:
  - Group related tests in classes
  - Use descriptive test names that explain the scenario
  - Follow AAA pattern (Arrange, Act, Assert)
  - Add docstrings for complex test scenarios

  5. Self-Assessment Prompts:
  "After generating tests, identify potential weaknesses:
  - Are mocks realistic?
  - Are edge cases comprehensive?
  - Would these tests catch real regressions?"

  6. PR Comment Generation:
  The LLM could generate structured review comments like:
  ⚠️ Review needed: Mock data in test_api_call() - validate against actual API responses
  🔍 Edge case: Consider testing with very large inputs
  ✅ Coverage: All public methods tested
"""
