"""TK prompts for Pydantic types."""

import typing

import tkinter.filedialog
import tkinter.messagebox
import pydantic

from ...api import register, prompt

PydanticModel = typing.TypeVar("PydanticModel", bound=pydantic.BaseModel)


@register(pydantic.BaseModel, interface="tk")
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
                interface="tk",
            )
            if field_value is None and field_info.is_required():
                tkinter.messagebox.showerror(
                    "Error", "Field is required. Please try again."
                )
                continue
            break
        field_dict[field_name] = field_value
    return data_type.model_validate(field_dict)


@register(pydantic.FilePath, interface="tk")
def prompt_file_path(
    message: str = "Select a file path.",
    data_type: type = pydantic.FilePath,
) -> pydantic.FilePath:
    adapter = pydantic.TypeAdapter(data_type)
    while True:
        path = tkinter.filedialog.askopenfilename(title=message, message=message)
        try:
            return adapter.validate_python(path)
        except pydantic.ValidationError:
            tkinter.messagebox.showerror(
                "Error", "Invalid input. Select a valid file path."
            )


@register(pydantic.DirectoryPath, interface="tk")
def prompt_directory_path(
    message: str = "Select a directory path.",
    data_type: type = pydantic.DirectoryPath,
) -> pydantic.DirectoryPath:
    adapter = pydantic.TypeAdapter(data_type)
    while True:
        path = tkinter.filedialog.askdirectory(title=message)
        try:
            return adapter.validate_python(path)
        except pydantic.ValidationError:
            tkinter.messagebox.showerror(
                "Error", "Invalid input. Select a valid directory path."
            )
