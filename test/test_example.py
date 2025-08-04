import pytest
from src.example import add_numbers, greet

def test_add_numbers_positive():
    """Test adding two positive numbers."""
    assert add_numbers(3, 5) == 8

def test_add_numbers_negative():
    """Test adding a positive and a negative number."""
    assert add_numbers(10, -4) == 6

def test_add_numbers_zero():
    """Test adding zero to a number."""
    assert add_numbers(7, 0) == 7

def test_add_numbers_large():
    """Test adding large numbers."""
    assert add_numbers(1000000, 2000000) == 3000000

def test_greet_normal_name():
    """Test greeting with a standard name."""
    assert greet("Alice") == "Hello, Alice!"

def test_greet_empty_name():
    """Test greeting with an empty string."""
    assert greet("") == "Hello, !"

def test_greet_with_spaces():
    """Test greeting with a name containing spaces."""
    assert greet("John Doe") == "Hello, John Doe!"

def test_greet_with_special_characters():
    """Test greeting with a name containing special characters."""
    assert greet("Alice_Smith-123") == "Hello, Alice_Smith-123!"