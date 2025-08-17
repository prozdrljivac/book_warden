from apps.validators import (
    is_strict_integer,
    is_positive_strict_integer,
    is_non_negative_strict_integer
)


class TestIsStrictInteger:
    def test_valid_integers(self):
        valid_integers = [0, 1, -1, 42, -42, 999999, -999999]
        for value in valid_integers:
            assert is_strict_integer(value), f"Failed for {value}"

    def test_non_integers_rejected(self):
        non_integers = [
            3.14,           # float
            "123",          # string
            [1, 2, 3],      # list
            {"key": 1},     # dict
            None,           # None
            (1, 2),         # tuple
            {1, 2, 3},      # set
            True,           # bool
            False           # bool
        ]

        for value in non_integers:
            assert not is_strict_integer(value), f"Failed for {value}"


class TestIsPositiveStrictInteger:
    def test_positive_integers(self):
        positive_integers = [1, 2, 42, 999999]
        for value in positive_integers:
            assert is_positive_strict_integer(value), f"Failed for {value}"

    def test_zero_and_negative_rejected(self):
        non_positive = [0, -1, -42, -999999]
        for value in non_positive:
            assert not is_positive_strict_integer(value), f"Failed for {value}"

    def test_non_integers_rejected(self):
        non_integers = [3.14, "1", [1], None, True, False]
        for value in non_integers:
            assert not is_positive_strict_integer(value), f"Failed for {value}"


class TestIsNonNegativeStrictInteger:
    def test_non_negative_integers(self):
        non_negative_integers = [0, 1, 2, 42, 999999]
        for value in non_negative_integers:
            assert is_non_negative_strict_integer(value), f"Failed for {value}"

    def test_negative_integers_rejected(self):
        negative_integers = [-1, -2, -42, -999999]
        for value in negative_integers:
            assert not is_non_negative_strict_integer(value), f"Failed for {value}"

    def test_non_integers_rejected(self):
        non_integers = [3.14, "0", [0], None, True, False]
        for value in non_integers:
            assert not is_non_negative_strict_integer(value), f"Failed for {value}"
