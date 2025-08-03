# SYSTEM_PROMPT = """You are a Python test generator. Analyze the provided code and generate comprehensive unit tests."""

# TEST_GENERATION_PROMPT = """
# Analyze this Python file and generate pytest unit tests:

# File: {file_path}
# Content: {file_content}

# Requirements:
# - Use pytest framework
# - Test all public functions
# - Include edge cases
# """

TEST_GENERATION_PROMPT = """
Can you tell me the methods that are in this file?

File: {file_path}
"""
