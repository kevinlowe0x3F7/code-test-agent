import pytest
from src.example import add_numbers, greet

def test_add_numbers_positive():
    """Test adding two positive numbers."""
    assert add_numbers(3, 5) == 8

def test_add_numbers_negative():
    """Test adding a positive and negative number."""
    assert add_numbers(10, -4) == 6

def test_add_numbers_zero():
    """Test adding with zero."""
    assert add_numbers(0, 0) == 0

def test_add_numbers_type_hints():
    """Verify that the function accepts integer type hints."""
    result = add_numbers(2, 3)
    assert isinstance(result, int)

def test_greet_basic():
    """Test basic greeting functionality."""
    assert greet("Alice") == "Hello, Alice!"

def test_greet_empty_string():
    """Test greeting with an empty string."""
    assert greet("") == "Hello, !"

def test_greet_whitespace():
    """Test greeting with whitespace name."""
    assert greet(" John ") == "Hello,  John !"

def test_greet_type_hints():
    """Verify that the function accepts string type hint."""
    result = greet("Bob")
    assert isinstance(result, str)