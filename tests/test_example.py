"""
Example test file for CI/CD pipeline
"""
import pytest


def test_example():
    """Example test that always passes"""
    assert True


def test_addition():
    """Test basic addition"""
    assert 1 + 1 == 2


def test_string_operations():
    """Test string operations"""
    text = "Hello, World!"
    assert "Hello" in text
    assert len(text) > 0
