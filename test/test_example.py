import pytest
from src.example import add_numbers, greet


def test_add_numbers_positive():
    assert add_numbers(2, 3) == 5


def test_add_numbers_negative():
    assert add_numbers(-2, 3) == 1


def test_add_numbers_zer():
    assert add_numbers(0, 0) == 0


def test_greet_name():
    assert greet("Alice") == "Hello, Alice!"


def test_greet_empty_name():
    assert greet("") == "Hello, !"
