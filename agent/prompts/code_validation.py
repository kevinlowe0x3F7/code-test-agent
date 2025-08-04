CODE_VALIDATION_PROMPT = """
  CRITICAL: Tests are failing. You MUST fix them using apply_diff_file tool.

  pytest results: {pytest_result}

  REQUIRED ACTIONS:
  1. Identify the exact syntax/logic errors from pytest output
  2. Use apply_diff_file tool to fix each error
  3. Do NOT just read files - you must EXECUTE fixes

  The pytest error shows exactly what's wrong.

  The apply_diff_file tool expects a unified diff format. Example:
  1. Line Change (Most Common)

  --- a/test/test_example.py
  +++ b/test/test_example.py
  @@ -6,1 +6,1 @@
  -    assert add_numbers(2, 3) == 6
  +    assert add_numbers(2, 3) == 5

  2. Line Addition

  --- a/test/test_example.py
  +++ b/test/test_example.py
  @@ -10,0 +11,1 @@
  +    assert add_numbers(5, 5) == 10

  3. Line Removal

  --- a/test/test_example.py
  +++ b/test/test_example.py
  @@ -18,1 +17,0 @@
  -    assert greet("Bob") == "Hello, Bob!"

  4. Multiple Changes in One Hunk

  --- a/test/test_example.py
  +++ b/test/test_example.py
  @@ -5,3 +5,4 @@
   def test_add_numbers_positive():
  -    assert add_numbers(2, 3) == 6
  +    assert add_numbers(2, 3) == 5
  +    assert add_numbers(1, 1) == 2

  Critical Format Rules:

  1. Header Format (EXACT):
  --- a/test/test_example.py
  +++ b/test/test_example.py

  2. Hunk Header Format:
  @@ -old_start,old_count +new_start,new_count @@

  3. Line Prefixes:
  -   (space) = Context line (unchanged)
  - - = Remove this line
  - + = Add this line
  """
