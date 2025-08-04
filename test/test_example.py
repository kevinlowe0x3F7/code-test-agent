import pytest
from src.example import add_numbers, greet

def test_add_numbers_positive():
    """Test adding two positive numbers."""
    assert add_numbers(3, 5) == 8

def test_add_numbers_negative():
    """Test adding a positive and a negative number."""
    assert add_numbers(10, -4) == 6

def test_add_numbers_zero():
    """Test adding numbers with zero."""
    assert add_numbers(0, 0) == 0
    assert add_numbers(7, 0) == 7

def test_greet_basic():
    """Test basic greeting functionality."""
    assert greet("Alice") == "Hello, Alice!"

def test_greet_empty_string():
    """Test greeting with an empty string."""
    assert greet("") == "Hello, !"

def test_greet_with_spaces():
    """Test greeting with names containing spaces."""
    assert greet("John Doe") == "Hello, John Doe!"

def test_greet_with_special_characters():
    """Test greeting with names containing special characters."""
    assert greet("Alice_Smith-123") == "Hello, Alice_Smith-123!"