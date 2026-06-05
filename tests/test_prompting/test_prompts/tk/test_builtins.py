from unittest.mock import patch, MagicMock

import pytest

from src.beanapp.prompting.prompts.tk.builtins import (
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

pytest.importorskip("tkinter")


class TestStrPrompt:
    def test_returns_string(self):
        with patch("tkinter.simpledialog.askstring", return_value="hello"):
            assert prompt_str("test") == "hello"

    def test_returns_empty_string(self):
        with patch("tkinter.simpledialog.askstring", return_value=""):
            assert prompt_str("test") == ""

    def test_returns_none_when_cancelled(self):
        with patch("tkinter.simpledialog.askstring", return_value=None):
            assert prompt_str("test") is None


class TestIntPrompt:
    def test_returns_int(self):
        with (
            patch("tkinter.simpledialog.askinteger", return_value=42),
            patch("tkinter.messagebox.showerror"),
        ):
            assert prompt_int("test") == 42

    def test_retries_on_invalid(self):
        with (
            patch("tkinter.simpledialog.askinteger", side_effect=[None, 42]),
            patch("tkinter.messagebox.showerror"),
        ):
            assert prompt_int("test") == 42


class TestFloatPrompt:
    def test_returns_float(self):
        with (
            patch("tkinter.simpledialog.askfloat", return_value=3.14),
            patch("tkinter.messagebox.showerror"),
        ):
            assert prompt_float("test") == 3.14

    def test_retries_on_invalid(self):
        with (
            patch("tkinter.simpledialog.askfloat", side_effect=[None, 2.5]),
            patch("tkinter.messagebox.showerror"),
        ):
            assert prompt_float("test") == 2.5


class TestComplexPrompt:
    def test_parses_complex_string(self):
        with (
            patch("tkinter.simpledialog.askstring", return_value="1+2j"),
            patch("tkinter.messagebox.showerror"),
        ):
            assert prompt_complex("test") == (1 + 2j)


class TestBoolPrompt:
    def test_returns_yes_as_true(self):
        with (
            patch("tkinter.messagebox.askyesno", return_value=True),
            patch("tkinter.messagebox.showerror"),
        ):
            assert prompt_bool("test") is True

    def test_returns_no_as_false(self):
        with (
            patch("tkinter.messagebox.askyesno", return_value=False),
            patch("tkinter.messagebox.showerror"),
        ):
            assert prompt_bool("test") is False


class TestListPrompt:
    def test_returns_list_from_scrolled_text(self):
        with patch(
            "src.beanapp.prompting.prompts.tk.builtins.ScrolledTextDialog",
            return_value=MagicMock(result="a\nb\nc"),
        ):
            assert prompt_list("test") == ["a", "b", "c"]

    def test_returns_empty_list_when_cancelled(self):
        with patch(
            "src.beanapp.prompting.prompts.tk.builtins.ScrolledTextDialog",
            return_value=MagicMock(result=None),
        ):
            assert prompt_list("test") == []


class TestTuplePrompt:
    def test_returns_tuple_from_scrolled_text(self):
        with patch(
            "src.beanapp.prompting.prompts.tk.builtins.ScrolledTextDialog",
            return_value=MagicMock(result="a\nb"),
        ):
            assert prompt_tuple("test") == ("a", "b")


class TestSetPrompt:
    def test_returns_set_from_scrolled_text(self):
        with patch(
            "src.beanapp.prompting.prompts.tk.builtins.ScrolledTextDialog",
            return_value=MagicMock(result="a\nb\na"),
        ):
            assert prompt_set("test") == {"a", "b"}


class TestFrozensetPrompt:
    def test_returns_frozenset(self):
        with patch(
            "src.beanapp.prompting.prompts.tk.builtins.ScrolledTextDialog",
            return_value=MagicMock(result="a\nb"),
        ):
            result = prompt_frozenset("test")
            assert isinstance(result, frozenset)
            assert result == frozenset({"a", "b"})


class TestDictPrompt:
    def test_returns_dict_from_scrolled_text(self):
        with patch(
            "src.beanapp.prompting.prompts.tk.builtins.ScrolledTextDialog",
            return_value=MagicMock(result="a=1\nb=2"),
        ):
            assert prompt_dict("test") == {"a": "1", "b": "2"}
