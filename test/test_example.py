import pytest
from src.example import add_numbers, greet

def test_add_numbers_positive():
    """Test adding two positive numbers."""
    assert add_numbers(2, 3) == 5

def test_add_numbers_negative():
    """Test adding negative numbers."""
    assert add_numbers(-2, -3) == -5

def test_add_numbers_mixed():
    """Test adding a positive and negative number."""
    assert add_numbers(5, -3) == 2

def test_add_numbers_zero():
    """Test adding zero."""
    assert add_numbers(0, 0) == 0
    assert add_numbers(10, 0) == 10

def test_add_numbers_large():
    """Test adding large numbers."""
    assert add_numbers(1000000, 2000000) == 3000000

def test_greet_basic():
    """Test basic greeting functionality."""
    assert greet("Alice") == "Hello, Alice!"

def test_greet_empty_string():
    """Test greeting with an empty string."""
    assert greet("") == "Hello, !"

def test_greet_with_spaces():
    """Test greeting with names containing spaces."""
    assert greet("John Doe") == "Hello, John Doe!"

def test_greet_special_characters():
    """Test greeting with special characters in name."""
    assert greet("Alice_Smith-123") == "Hello, Alice_Smith-123!"