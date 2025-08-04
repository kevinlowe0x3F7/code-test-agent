import pytest
from src.example import add_numbers, greet


def test_add_numbers_positive():
    """Test adding two positive numbers."""
    assert add_numbers(3, 5) == 8


def test_add_numbers_negative():
    """Test adding positive and negative numbers."""
    assert add_numbers(10, -4) == 6


def test_add_numbers_zero():
    """Test adding numbers with zero."""
    assert add_numbers(0, 0) == 0
    assert add_numbers(7, 0) == 7


def test_greet_normal_name():
    """Test greeting with a normal name."""
    assert greet("Alice") == "Hello, Alice!"


def test_greet_empty_string():
    """Test greeting with an empty string."""
    assert greet("") == "Hello, !"


def test_greet_invalid_type():
    """Test greeting with an invalid type raises TypeError."""
    with pytest.raises(TypeError, match="Name must be a string"):
        greet(123)
    with pytest.raises(TypeError, match="Name must be a string"):
        greet(None)