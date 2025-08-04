from langchain_core.tools import tool
import patch


@tool
def apply_diff_file(test_file_path: str, unified_diff: str) -> str:
    """
    Apply a unified diff format to a file.
    """
    try:
        if test_file_path not in unified_diff:
            return f"Error: Diff doesn't target {test_file_path}"
        elif not unified_diff:
            return f"Error: didn't get a unified diff for {test_file_path}"

        # Convert string to bytes for patch library
        patch_set = patch.fromstring(unified_diff.encode("utf-8"))

        # Apply the patch (modifies files based on diff headers)
        success = patch_set.apply(root=".")

        if success:
            return f"Successfully applied diff to {test_file_path}"
        else:
            return f"Failed to apply diff to {test_file_path} - patch conflicts"

    except Exception as e:
        return f"Error applying diff to {test_file_path}: {e}"
