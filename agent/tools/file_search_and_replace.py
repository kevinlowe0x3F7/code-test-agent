from typing import List, Dict
from langchain_core.tools import tool
from pydantic import BaseModel


class SearchReplaceOperation(BaseModel):
    old_pattern: str
    new_pattern: str


def _search_and_replace_impl(file_path: str, operations: List[Dict[str, str]]) -> str:
    """Apply multiple search-and-replace operations to a file in sequence."""
    try:
        with open(file_path, "r") as f:
            content = f.read()
        
        original_content = content
        modifications_made = []
        
        for i, op in enumerate(operations):
            old_pattern = op["old_pattern"]
            new_pattern = op["new_pattern"]
            
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                modifications_made.append(f"Operation {i+1}: Replaced '{old_pattern}' with '{new_pattern}'")
            else:
                modifications_made.append(f"Operation {i+1}: Pattern '{old_pattern}' not found - skipped")
        
        # Write the modified content back
        with open(file_path, "w") as f:
            f.write(content)
        
        if content != original_content:
            result = f"Successfully modified {file_path}:\n" + "\n".join(modifications_made)
        else:
            result = f"No changes made to {file_path} - no patterns matched"
            
        return result
        
    except Exception as e:
        return f"Error processing {file_path}: {e}"


@tool
def search_and_replace_in_file(file_path: str, operations: List[Dict[str, str]]) -> str:
    """
    Apply multiple search-and-replace operations to a file.
    
    Args:
        file_path: Path to the file to modify
        operations: List of dicts with 'old_pattern' and 'new_pattern' keys
        
    Example:
        operations = [
            {"old_pattern": "assert add_numbers(-2, 3) == 1", "new_pattern": "assert add_numbers(-2, 3) == 1"},
            {"old_pattern": "import pytest", "new_pattern": "import pytest\nfrom unittest.mock import Mock"}
        ]
    """
    return _search_and_replace_impl(file_path, operations)