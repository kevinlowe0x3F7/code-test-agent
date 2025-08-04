import pytest
from src.example import add_numbers, greet

def test_add_numbers_positive():
    """Test adding two positive numbers."""
    assert add_numbers(3, 5) == 8

def test_add_numbers_negative():
    """Test adding a negative and a positive number."""
    assert add_numbers(-3, 5) == 2

def test_add_numbers_zero():
    """Test adding zero to a number."""
    assert add_numbers(0, 10) == 10

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
    """Test greeting with a name containing spaces."""
    assert greet("John Doe") == "Hello, John Doe!"

def test_greet_special_characters():
    """Test greeting with special characters in the name."""
    assert greet("Alice-Bob") == "Hello, Alice-Bob!"