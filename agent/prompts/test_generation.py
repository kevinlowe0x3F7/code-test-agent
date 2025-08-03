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
