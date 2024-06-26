# tests/test_sample.py

import pytest


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y


# 测试加法函数
def test_add():
    assert add(3, 5) == 8
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2


# 测试减法函数
def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(-1, 1) == -2
    assert subtract(-1, -1) == 0


# 测试乘法函数
def test_multiply():
    assert multiply(3, 5) == 15
    assert multiply(-1, 1) == -1
    assert multiply(-1, -1) == 1


# 测试除法函数
def test_divide():
    assert divide(10, 2) == 5
    assert divide(10, -2) == -5
    assert divide(-10, -2) == 5
    with pytest.raises(ValueError):
        divide(10, 0)
