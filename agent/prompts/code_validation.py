CODE_VALIDATION_PROMPT = """
  CRITICAL: Tests are failing. You MUST fix them using search_and_replace_in_file tool.

  pytest results: {pytest_result}

  REQUIRED ACTIONS:
  1. Identify the exact syntax/logic errors from pytest output
  2. Use search_and_replace_in_file tool to fix each error
  3. Do NOT just read files - you must EXECUTE fixes

  The pytest error shows exactly what's wrong. Fix it immediately.

  For the search_and_replace_in_file_tool, you pass in the test file path and the
  operations list. Each operation should have 'old_pattern' and 'new_pattern' keys.

  Example:
  [
      {{"old_pattern": "assert add_numbers(-2, 3) == 2", "new_pattern": "assert add_numbers(-2, 3) == 1"}},
      {{"old_pattern": "from src.exampl", "new_pattern": "from src.example"}}
  ]
  """
