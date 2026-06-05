from unittest.mock import patch

from src.beanapp import config, modes
from src.beanapp.prompting.prompts.cli.beanapp import (
    prompt_log_level,
    prompt_program_mode,
)


class TestLogLevelPrompt:
    def test_parses_valid_level(self):
        with patch("builtins.input", lambda _: "INFO"), patch("builtins.print"):
            result = prompt_log_level()
            assert result == config.LogLevel.INFO


class TestProgramModePrompt:
    def test_selects_mode_by_index(self):
        modes.AVAILABLE_MODES.clear()
        try:
            mode = modes.ProgramMode(
                name="test_mode",
                description="desc",
                config_class=type("C", (), {}),
                entry_point="does.not.exist",
            )
            with patch("builtins.input", lambda _: "1"), patch("builtins.print"):
                result = prompt_program_mode()
            assert result is mode
        finally:
            modes.AVAILABLE_MODES.clear()
