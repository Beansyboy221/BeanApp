from unittest.mock import patch, MagicMock

import pytest

from src.beanapp.prompting.prompts.tk.typing import prompt_union

pytest.importorskip("tkinter")


class TestUnionTypePrompt:
    def test_selects_type_from_listbox(self):
        with (
            patch(
                "src.beanapp.prompting.prompts.tk.typing.SelectDialog",
                return_value=MagicMock(result="int"),
            ),
            patch("tkinter.simpledialog.askinteger", return_value=42),
            patch("tkinter.messagebox.showerror"),
        ):
            result = prompt_union("test", int | str)

        assert result == 42

    def test_retries_on_invalid_choice(self):
        with (
            patch(
                "src.beanapp.prompting.prompts.tk.typing.SelectDialog",
                side_effect=[MagicMock(result=None), MagicMock(result="int")],
            ),
            patch("tkinter.simpledialog.askinteger", return_value=42),
            patch("tkinter.messagebox.showerror"),
        ):
            result = prompt_union("test", int | str)

        assert result == 42
