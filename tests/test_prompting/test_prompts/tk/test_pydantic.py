from unittest.mock import patch

import pydantic
import pytest

from src.beanapp.prompting.prompts.tk.pydantic import (
    prompt_file_path,
    prompt_directory_path,
    prompt_pydantic_model,
)

pytest.importorskip("tkinter")


class TestFilePathPrompt:
    def test_returns_validated_file_path(self):
        with (
            patch("tkinter.filedialog.askopenfilename", return_value=__file__),
            patch("tkinter.messagebox.showerror"),
        ):
            result = prompt_file_path("test")
            assert result == pydantic.FilePath(__file__)


class TestDirectoryPathPrompt:
    def test_returns_validated_directory_path(self):
        import pathlib

        parent_dir = pathlib.Path(__file__).parent
        with (
            patch("tkinter.filedialog.askdirectory", return_value=str(parent_dir)),
            patch("tkinter.messagebox.showerror"),
        ):
            result = prompt_directory_path("test")
            assert result == pydantic.DirectoryPath(parent_dir)


class TestPydanticModelPrompt:
    def test_populates_fields(self):
        class TestModel(pydantic.BaseModel):
            name: str
            age: int

        with (
            patch("tkinter.simpledialog.askstring", return_value="Alice"),
            patch("tkinter.simpledialog.askinteger", return_value=21),
            patch("tkinter.messagebox.showerror"),
        ):
            result = prompt_pydantic_model("test", TestModel)

        assert isinstance(result, TestModel)
        assert result.name == "Alice"
        assert result.age == 21

    def test_mro_fallback_resolves_concrete_model(self):
        class AppConfig(pydantic.BaseModel):
            app_name: str
            version: int

        with (
            patch("tkinter.simpledialog.askstring", return_value="BeanApp"),
            patch("tkinter.simpledialog.askinteger", return_value=1),
            patch("tkinter.messagebox.showerror"),
        ):
            result = prompt_pydantic_model(data_type=AppConfig)

        assert isinstance(result, AppConfig)
        assert result.app_name == "BeanApp"
        assert result.version == 1
