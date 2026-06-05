from unittest.mock import patch

from src.beanapp.prompting.prompts.cli.typing import prompt_union


class TestUnionTypePrompt:
    def test_selects_type_and_prompts(self):
        inputs = iter(["1", "42"])
        with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
            result = prompt_union("test", int | str)

        assert result == 42

    def test_retries_on_invalid_choice(self):
        inputs = iter(["3", "1", "42"])
        with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
            result = prompt_union("test", int | str)

        assert result == 42
