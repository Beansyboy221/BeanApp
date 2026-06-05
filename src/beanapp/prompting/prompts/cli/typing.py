"""CLI prompts for typing module types."""

import typing
import types

from ...api import prompt, register


@register(types.UnionType)
def prompt_union(
    message: str = "Choose a type.",
    data_type: type = types.UnionType,
) -> typing.Any:
    unioned_types = typing.get_args(data_type)
    options = {
        str(index): unioned_type
        for index, unioned_type in enumerate(unioned_types, start=1)
    }
    print(f"\n{message}")
    for index, typ in options.items():
        print(f"  [{index}] {typ.__name__}")
    while True:
        choice = input("Enter the index of the type you want: ").strip()
        if choice in options:
            return prompt(options[choice])
        print(f"Invalid choice. Choose: {', '.join(options)}")
