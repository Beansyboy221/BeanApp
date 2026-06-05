"""CLI prompts for Pydantic types."""

import typing

import pydantic

from ...api import register, prompt
from . import builtins

PydanticModel = typing.TypeVar("PydanticModel", bound=pydantic.BaseModel)


@register(pydantic.BaseModel)
def prompt_pydantic_model(
    message: str = "Populate this pydantic model.",
    data_type: type[PydanticModel] = pydantic.BaseModel,
) -> PydanticModel:
    field_dict = {}
    for field_name, field_info in data_type.model_fields.items():
        while True:
            if field_info.annotation is None:
                raise TypeError(
                    f"Field: {field_name} is missing type annotation for prompting."
                )
            field_value = prompt(
                data_type=field_info.annotation,
                message=field_info.description,
            )
            if field_value is None and field_info.is_required():
                print("Field is required. Please try again.")
                continue
            break
        field_dict[field_name] = field_value
    return data_type.model_validate(field_dict)


@register(pydantic.FilePath)
def prompt_file_path(
    message: str = "Enter a file path.",
    data_type: type = pydantic.FilePath,
) -> pydantic.FilePath:
    adapter = pydantic.TypeAdapter(data_type)
    while True:
        path = builtins.prompt_str(message)
        try:
            return adapter.validate_python(path)
        except pydantic.ValidationError:
            print("Invalid input. Enter a valid file path.")


@register(pydantic.DirectoryPath)
def prompt_directory_path(
    message: str = "Enter a directory path.",
    data_type: type = pydantic.DirectoryPath,
) -> pydantic.DirectoryPath:
    adapter = pydantic.TypeAdapter(data_type)
    while True:
        path = builtins.prompt_str(message)
        try:
            return adapter.validate_python(path)
        except pydantic.ValidationError:
            print("Invalid input. Enter a valid directory path.")
