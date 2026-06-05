"""TK prompts for typing module types."""

import tkinter.messagebox
import typing
import types

from ...api import register, prompt
from ...dialogs import SelectDialog


@register(types.UnionType, interface="tk")
def prompt_union(
    message: str = "Choose a type.",
    data_type: type = types.UnionType,
) -> typing.Any:
    unioned_types = typing.get_args(data_type)
    type_names = [unioned_type.__name__ for unioned_type in unioned_types]
    while True:
        result = SelectDialog("Input", message, type_names).result
        if result is None:
            tkinter.messagebox.showerror("Cannot select nothing. Please try again.")
            continue
        selected_type = unioned_types[type_names.index(result)]
        return prompt(selected_type, interface="tk")
