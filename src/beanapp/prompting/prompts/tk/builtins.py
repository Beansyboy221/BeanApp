"""TK prompts for built-in Python types using tkinter.simpledialog."""

import typing

import tkinter.simpledialog as sd
import tkinter.messagebox

from ...api import register, prompt
from ...dialogs import ScrolledTextDialog, SelectDialog


@register(str, interface="tk")
def prompt_str(
    message: str = "Enter a string.",
    data_type: type = str,
) -> str:
    return sd.askstring("Input", message)


@register(int, interface="tk")
def prompt_int(
    message: str = "Enter an integer.",
    data_type: type = int,
) -> int:
    while True:
        result = sd.askinteger("Input", message)
        if result is not None:
            return result
        tkinter.messagebox.showerror("Invalid input. Enter an integer.")


@register(float, interface="tk")
def prompt_float(
    message: str = "Enter a number.",
    data_type: type = float,
) -> float:
    while True:
        result = sd.askfloat("Input", message)
        if result is not None:
            return result
        tkinter.messagebox.showerror("Invalid input. Enter a number.")


@register(complex, interface="tk")
def prompt_complex(
    message: str = "Enter a complex number (e.g., 1+2j).",
    data_type: type = complex,
) -> complex:
    while True:
        result = prompt_str(message)
        if result is None:
            return None
        try:
            return complex(result.replace(" ", ""))
        except ValueError:
            tkinter.messagebox.showerror(
                "Error", "Invalid format. Use a+bj (e.g., 3+4j)."
            )


@register(bool, interface="tk")
def prompt_bool(
    message: str = "Enter True or False.",
    data_type: type = bool,
) -> bool:
    return tkinter.messagebox.askyesno("Input", message)


@register(list, interface="tk")
def prompt_list(
    message="Enter a list of values.",
    data_type: type = list,
) -> list:
    element_types = typing.get_args(data_type)
    if not element_types:
        result = ScrolledTextDialog("Input", message).result
        return result.splitlines() if result else []
    element_type = element_types[0]
    result = []
    while True:
        element = prompt(element_type, interface="tk")
        if element is None:
            break
        result.append(element)
        if not prompt_bool("Add another element?"):
            break
    return result


@register(tuple, interface="tk")
def prompt_tuple(
    message="Enter a list of values.",
    data_type: type = tuple,
) -> tuple:
    element_types = typing.get_args(data_type)
    if not element_types:
        result = ScrolledTextDialog("Input", message).result
        return tuple(result.splitlines()) if result else ()
    type_names = [
        f"[{index}] {element_type.__name__}"
        for index, element_type in enumerate(element_types)
    ]
    result = []
    while True:
        result = SelectDialog("Input", "Select element type:", type_names).result
        if result is None:
            break
        selected_index = type_names.index(result)
        element = prompt(element_types[selected_index], interface="tk")
        if element is None:
            break
        result.append(element)
        if not prompt_bool("Add another element?"):
            break
    return tuple(result)


@register(set, interface="tk")
def prompt_set(
    message="Enter a set of values.",
    data_type: type = set,
) -> set:
    element_types = typing.get_args(data_type)
    if not element_types:
        result = ScrolledTextDialog("Input", message).result
        return set(result.splitlines()) if result else set()
    element_type = element_types[0]
    result = set()
    while True:
        element = prompt(element_type, interface="tk")
        if element is None:
            break
        result.add(element)
        if not prompt_bool("Add another element?"):
            break
    return result


@register(frozenset, interface="tk")
def prompt_frozenset(
    message="Enter a set of values.",
    data_type: type = frozenset,
) -> frozenset:
    return frozenset(prompt_set(message=message))


@register(dict, interface="tk")
def prompt_dict(
    message="Enter key=value pairs.",
    data_type: type = dict,
) -> dict:
    key_type, value_type = typing.get_args(data_type) or (None, None)
    if key_type is None:
        result = ScrolledTextDialog("Input", message).result
        if result is None:
            return {}
        pairs = {}
        for line in result.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                pairs[k.strip()] = v.strip()
        return pairs
    result = {}
    while True:
        key = prompt(key_type, interface="tk")
        if key is None:
            break
        value = prompt(value_type, interface="tk")
        if value is None:
            break
        result[key] = value
        if not prompt_bool("Add another pair?"):
            break
    return result
