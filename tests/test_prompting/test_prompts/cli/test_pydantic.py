from unittest.mock import patch

import pydantic

from src.beanapp.prompting.prompts.cli.pydantic import (
    prompt_pydantic_model,
    prompt_file_path,
    prompt_directory_path,
)


class TestFilePathPrompt:
    def test_returns_validated_file_path(self):
        with patch("builtins.input", lambda _: __file__), patch("builtins.print"):
            result = prompt_file_path("test")
            assert result == pydantic.FilePath(__file__)


class TestDirectoryPathPrompt:
    def test_returns_validated_directory_path(self):
        import pathlib

        dir_path = pathlib.Path(__file__).parent
        with patch("builtins.input", lambda _: str(dir_path)), patch("builtins.print"):
            result = prompt_directory_path("test")
            assert result == pydantic.DirectoryPath(dir_path)


class TestPydanticModelPrompt:
    def test_populates_fields(self):
        class TestModel(pydantic.BaseModel):
            name: str
            age: int

        inputs = iter(["Alice", "30"])
        with (
            patch("builtins.input", lambda _: next(inputs)),
            patch("builtins.print"),
        ):
            result = prompt_pydantic_model(data_type=TestModel)

        assert isinstance(result, TestModel)
        assert result.name == "Alice"
        assert result.age == 30

    def test_mro_fallback_resolves_concrete_model(self):
        class AppConfig(pydantic.BaseModel):
            app_name: str
            version: int

        inputs = iter(["BeanApp", "1"])
        with (
            patch("builtins.input", lambda _: next(inputs)),
            patch("builtins.print"),
        ):
            result = prompt_pydantic_model(data_type=AppConfig)

        assert isinstance(result, AppConfig)
        assert result.app_name == "BeanApp"
        assert result.version == 1
