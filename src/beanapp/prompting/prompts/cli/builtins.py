"""CLI prompts for built-in Python types."""

import typing

from ...api import prompt, register


@register(str)
def prompt_str(
    message: str = "Enter a string.",
    data_type: type = str,
) -> str:
    return input(f"\n{message}\n")


@register(int)
def prompt_int(
    message: str = "Enter an integer (e.g., 42).",
    data_type: type = int,
) -> int:
    while True:
        try:
            return int(prompt_str(message))
        except ValueError:
            print("Invalid input. Enter an integer (e.g., 42).")


@register(float)
def prompt_float(
    message: str = "Enter a number.",
    data_type: type = float,
) -> float:
    while True:
        try:
            return float(prompt_str(message))
        except ValueError:
            print("Invalid input. Enter a decimal or integer (e.g., 3.14).")


@register(complex)
def prompt_complex(
    message: str = "Enter a complex number (e.g., 1+2j).",
    data_type: type = complex,
) -> complex:
    while True:
        try:
            return complex(prompt_str(message))
        except ValueError:
            print("Invalid format. Use a+bj (e.g., 3+4j).")


@register(bool)
def prompt_bool(
    message: str = "Enter a bool (true/false, t/f, yes/no, y/n, or 1/0).",
    data_type: type = bool,
) -> bool:
    bool_strings = {
        "true": True,
        "t": True,
        "1": True,
        "yes": True,
        "y": True,
        "false": False,
        "f": False,
        "0": False,
        "no": False,
        "n": False,
    }
    while True:
        result = prompt_str(message).strip().lower()
        try:
            return bool_strings[result]
        except KeyError:
            print("Invalid input. Enter true/false, t/f, yes/no, y/n, or 1/0.")


@register(list)
def prompt_list(
    message="Enter a list of values.",
    data_type: type = list,
) -> list:
    element_types = typing.get_args(data_type)
    if not element_types:
        return prompt_str(message).split()
    element_type = element_types[0]
    result = []
    while True:
        if not prompt_bool("Add another element? (y/n)"):
            break
        element = prompt(element_type)
        result.append(element)
    return result


@register(tuple)
def prompt_tuple(
    message="Enter a list of values.",
    data_type: type = tuple,
) -> tuple:
    element_types = typing.get_args(data_type)
    if not element_types:
        return prompt_str(message).split()
    options = {
        str(index): unioned_type
        for index, unioned_type in enumerate(element_types, start=1)
    }
    print(f"\n{message}")
    for index, typ in options.items():
        print(f"  [{index}] {typ.__name__}")
    result = []
    while True:
        if not prompt_bool("Add another element? (y/n)"):
            break
        choice = input("Enter the index of the type you want to add: ").strip()
        if choice in options:
            element = prompt(options[choice])
            result.append(element)
        else:
            print(f"Invalid choice. Choose: {', '.join(options)}")
    return tuple(result)


@register(set)
def prompt_set(
    message="Enter a set of values.",
    data_type: type = set,
) -> set:
    element_types = typing.get_args(data_type)
    if not element_types:
        return set(prompt_str(message).split())
    element_type = element_types[0]
    result = set()
    while True:
        if not prompt_bool("Add another element? (y/n)"):
            break
        element = prompt(element_type)
        result.add(element)
    return result


@register(frozenset)
def prompt_frozenset(
    message="Enter a frozenset of values.",
    data_type: type = frozenset,
) -> frozenset:
    return frozenset(prompt_set(message=message))


@register(dict)
def prompt_dict(
    message="Enter key=value pairs.",
    data_type: type = dict,
) -> dict:
    key_type, value_type = typing.get_args(data_type) or (None, None)
    if key_type is None:
        result = {}
        for pair in prompt_str(message).split(","):
            pair = pair.strip()
            if "=" in pair:
                k, v = pair.split("=", 1)
                result[k.strip()] = v.strip()
        return result
    result = {}
    while True:
        if not prompt_bool("Add another pair? (y/n)"):
            break
        key = prompt(key_type)
        value = prompt(value_type)
        result[key] = value
    return result
