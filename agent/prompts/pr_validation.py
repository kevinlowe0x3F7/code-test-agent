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
  Remember that lines in files are 1-indexed, so that means if the comment is referring to line 3, then it is the 3rd line
  that should be added, removed, or modified, not the 4th line.
  {line_comments}

  REQUIRED ACTIONS:
  1. Read through all the comments to understand what changes need to made to the test file
  2. Read the contents of the test file using the read_file tool to get the latest output
  3. Address the comments by regenerating the file contents and overwriting using the write_file tool
  4. The changes should address ALL feedback provided

  IMPORTANT: Do not make any other extraneous changes to the file other than what is requested in comments

  IMPORTANT: When calling write_file, you MUST include both parameters:
  - file_path: "{test_file_path}"
  - content: "<your complete generated test code>"
  """
