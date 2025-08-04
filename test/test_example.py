import pytest
from src.example import add_numbers, greet

def test_add_numbers_positive():
    """Test adding positive numbers."""
    assert add_numbers(2, 3) == 5

def test_add_numbers_negative():
    """Test adding negative numbers."""
    assert add_numbers(-2, -3) == -5

def test_add_numbers_mixed():
    """Test adding positive and negative numbers."""
    assert add_numbers(5, -3) == 2

def test_add_numbers_zero():
    """Test adding zero."""
    assert add_numbers(0, 5) == 5
    assert add_numbers(5, 0) == 5
    assert add_numbers(0, 0) == 0

def test_greet_normal_name():
    """Test greeting with a regular name."""
    assert greet("Alice") == "Hello, Alice!"

def test_greet_empty_name():
    """Test greeting with an empty string."""
    assert greet("") == "Hello, !"

def test_greet_with_spaces():
    """Test greeting with a name containing spaces."""
    assert greet("John Doe") == "Hello, John Doe!"

def test_greet_with_special_characters():
    """Test greeting with a name containing special characters."""
    assert greet("Alice_123") == "Hello, Alice_123!"