"""
Type validation utilities

This module provides strict type checking functions that avoid common Python
pitfalls, such as bool being a subclass of int.
"""

from typing import Any


def is_strict_integer(value: Any) -> bool:
    """
    Check if a value is a genuine integer, excluding boolean values.

    In Python, bool is a subclass of int, which can lead to unexpected behavior:
    - isinstance(True, int) returns True
    - isinstance(False, int) returns True

    This function provides strict integer validation that excludes booleans.
    """
    return isinstance(value, int) and not isinstance(value, bool)


def is_positive_strict_integer(value: Any) -> bool:
    """
    Check if a value is a genuine positive integer (> 0), excluding booleans.
    """
    return is_strict_integer(value) and value > 0


def is_non_negative_strict_integer(value: Any) -> bool:
    """
    Check if a value is a genuine non-negative integer (>= 0), excluding booleans.
    """
    return is_strict_integer(value) and value >= 0
