CODE_VALIDATION_PROMPT = """
  CRITICAL: Tests are failing. You MUST fix them using write_file tool.

  Test File: {test_file_path}
  pytest results: {pytest_result}

  REQUIRED ACTIONS:
  1. Identify the exact syntax/logic errors from pytest output
  2. Read the contents of the test file using the read_file tool to get the latest output
  3. Address the syntax/logic errors by regenerating the file contents and overwriting using the write_file tool
  4. Do NOT just read files - you must EXECUTE fixes

  IMPORTANT: When calling write_file, you MUST include both parameters:
  - file_path: "{test_file_path}"
  - content: "<your complete generated test code>"
  The pytest error shows exactly what's wrong.
  """
