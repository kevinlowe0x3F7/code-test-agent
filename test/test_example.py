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
    assert add_numbers(0, 0) == 0
    assert add_numbers(10, 0) == 10

def test_greet_standard_name():
    """Test greeting with a standard name."""
    assert greet("Alice") == "Hello, Alice!"

def test_greet_empty_name():
    """Test greeting with an empty string."""
    assert greet("") == "Hello, !"

def test_greet_special_characters():
    """Test greeting with special characters."""
    assert greet("John Doe") == "Hello, John Doe!"
    assert greet("José") == "Hello, José!"