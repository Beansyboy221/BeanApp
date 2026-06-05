from unittest.mock import patch

import pytest

from src.beanapp.prompting.prompts.cli.builtins import (
    prompt_str,
    prompt_int,
    prompt_float,
    prompt_complex,
    prompt_bool,
    prompt_list,
    prompt_tuple,
    prompt_set,
    prompt_frozenset,
    prompt_dict,
)


class TestStrPrompt:
    def test_reads_input(self):
        with patch("builtins.input", lambda _: "hello"):
            assert prompt_str("test") == "hello"

    def test_empty_string(self):
        with patch("builtins.input", lambda _: ""):
            assert prompt_str("test") == ""


class TestIntPrompt:
    def test_parses_integer(self):
        with patch("builtins.input", lambda _: "42"):
            assert prompt_int("test") == 42

    def test_retries_on_invalid(self):
        inputs = iter(["abc", "42"])
        with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
            assert prompt_int("test") == 42


class TestFloatPrompt:
    def test_parses_float(self):
        with patch("builtins.input", lambda _: "3.14"):
            assert prompt_float("test") == 3.14

    def test_retries_on_invalid(self):
        inputs = iter(["not_a_number", "2.5"])
        with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
            assert prompt_float("test") == 2.5


class TestComplexPrompt:
    def test_parses_complex(self):
        with patch("builtins.input", lambda _: "1+2j"):
            assert prompt_complex("test") == (1 + 2j)


class TestBoolPrompt:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("true", True),
            ("t", True),
            ("1", True),
            ("yes", True),
            ("y", True),
            ("false", False),
            ("f", False),
            ("0", False),
            ("no", False),
            ("n", False),
        ],
    )
    def test_parses_bool_strings(self, raw, expected):
        with patch("builtins.input", lambda _: raw), patch("builtins.print"):
            assert prompt_bool("test") is expected

    def test_retries_on_invalid(self):
        inputs = iter(["maybe", "true"])
        with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
            assert prompt_bool("test") is True


class TestListPrompt:
    def test_returns_list_of_strings(self):
        with patch("builtins.input", lambda _: "a b c"), patch("builtins.print"):
            assert prompt_list("test") == ["a", "b", "c"]

    def test_returns_empty_list_for_empty_input(self):
        with patch("builtins.input", lambda _: ""), patch("builtins.print"):
            assert prompt_list("test") == []


class TestTuplePrompt:
    def test_returns_list_of_strings(self):
        with patch("builtins.input", lambda _: "a b"), patch("builtins.print"):
            assert prompt_tuple("test") == ["a", "b"]


class TestSetPrompt:
    def test_returns_set_of_strings(self):
        with patch("builtins.input", lambda _: "a b a"), patch("builtins.print"):
            assert prompt_set("test") == {"a", "b"}


class TestFrozensetPrompt:
    def test_returns_frozenset(self):
        with patch("builtins.input", lambda _: "a b"), patch("builtins.print"):
            result = prompt_frozenset("test")
            assert isinstance(result, frozenset)
            assert result == frozenset({"a", "b"})


class TestDictPrompt:
    def test_parses_key_value_pairs(self):
        with patch("builtins.input", lambda _: "a=1,b=2"), patch("builtins.print"):
            assert prompt_dict("test") == {"a": "1", "b": "2"}
