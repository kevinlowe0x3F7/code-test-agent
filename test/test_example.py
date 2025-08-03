import pytest
from src.example import add_numbers, greet

def test_add_numbers_positive():
    assert add_numbers(2, 3) == 5
    assert add_numbers(10, 20) == 30

def test_add_numbers_negative():
    assert add_numbers(-2, 3) == 1
    assert add_numbers(-5, -10) == -15

def test_add_numbers_zero():
    assert add_numbers(0, 0) == 0
    assert add_numbers(0, 10) == 10
    assert add_numbers(10, 0) == 10

def test_greet_simple():
    assert greet("Alice") == "Hello, Alice!"

def test_greet_empty_name():
    assert greet("") == "Hello, !"

def test_greet_whitespace_name():
    assert greet("  Bob  ") == "Hello,   Bob  !"