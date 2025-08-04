import pytest
from src.example import add_numbers, greet


def test_add_numbers_positive():
    """Test addition of two positive numbers."""
    assert add_numbers(3, 5) == 8


def test_add_numbers_negative():
    """Test addition of negative numbers."""
    assert add_numbers(-3, -5) == -8


def test_add_numbers_mixed():
    """Test addition of positive and negative numbers."""
    assert add_numbers(10, -7) == 3


def test_add_numbers_zero():
    """Test addition with zero."""
    assert add_numbers(0, 0) == 0
    assert add_numbers(5, 0) == 5
    assert add_numbers(0, -5) == -5


def test_greet_normal_name():
    """Test greeting with a normal name."""
    assert greet("Alice") == "Hello, Alice!"


def test_greet_empty_name():
    """Test greeting with an empty string."""
    assert greet("") == "Hello, !"


def test_greet_special_characters():
    """Test greeting with names containing special characters."""
    assert greet("John Doe") == "Hello, John Doe!"
    assert greet("O'Brien") == "Hello, O'Brien!"