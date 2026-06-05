from unittest.mock import patch, MagicMock

import pytest

from src.beanapp import config, modes
from src.beanapp.prompting.prompts.tk.beanapp import (
    prompt_log_level,
    prompt_program_mode,
)

pytest.importorskip("tkinter")


class TestLogLevelPrompt:
    def test_returns_log_level_from_combobox(self):
        with patch(
            "src.beanapp.prompting.prompts.tk.beanapp.SelectDialog",
            return_value=MagicMock(result="INFO"),
        ):
            assert prompt_log_level("test") == config.LogLevel.INFO


class TestProgramModePrompt:
    def test_selects_mode_from_listbox(self):
        modes.AVAILABLE_MODES.clear()
        try:
            mode = modes.ProgramMode(
                name="test_mode",
                description="desc",
                config_class=type("C", (), {}),
                entry_point="does.not.exist",
            )
            display = "test_mode - desc"
            with (
                patch(
                    "src.beanapp.prompting.prompts.tk.beanapp.SelectDialog",
                    return_value=MagicMock(result=display),
                ),
                patch("tkinter.messagebox.showerror"),
            ):
                result = prompt_program_mode("test")
                assert result is mode
        finally:
            modes.AVAILABLE_MODES.clear()
