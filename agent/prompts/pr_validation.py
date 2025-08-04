PR_COMMENT_RESPONSE_PROMPT = """
  You have received the following PR feedback that needs to be addressed:

  TOP-LEVEL REVIEW COMMENTS. These are comments given when the pull request review is submitted
  and is not specific to any particular line.
  {top_level_comments}

  LINE-SPECIFIC COMMENTS. Here is the information given for each line-specific comment:
  - body: The text content of the comment. The body might also contain suggestions. These are code snippets written by the reviewer
    themselves and taken highly into consideration as suggested changes.
  - path: The file path that this comment is relevant for
  - line: The line in the file that this comment is for
  - start_line: If this is present, that means that this is a comment that spans multiple lines. For example
    if line is 17 and start_line is 10, then this comment was meant for lines 10-17. If line is 17 and start_line
    is not present, then the comment is only for line 17.
  - diff_hunk: A unified diff that the comment refers to.
  {line_comments}

  REQUIRED ACTIONS:
  1. Address each comment by generating unified diff format changes
  2. Use apply_diff_file tool to make the changes
  3. The changes should address ALL feedback provided

  Here are examples of unified diff format:
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

  Generate appropriate diffs to address all feedback.
  """
