"""Public functions for interaction with the prompting package."""

import logging
import typing

logger = logging.getLogger("BeanApp Prompts")

AVAILABLE_PROMPTS: dict[tuple[type, str], typing.Callable] = {}
"""
A registry of all loaded prompts.\n
Keys: the prompt's type and the interface it uses (CLI, TK, etc.)
Value: the prompt reference
"""


def register(
    data_type: type,
    interface: str = "cli",
):
    """
    Decorator that registers a function as
    a prompt for the given data type and interface.\n
    Ensure all prompts are imported/registered before prompting.
    """

    def decorator(prompt):
        AVAILABLE_PROMPTS[(data_type, interface)] = prompt
        return prompt

    return decorator


def prompt(
    data_type: type,
    interface: str = "cli",
    message: str | None = None,
) -> typing.Any:
    """Automatically finds the right prompt for your data type."""
    prompt = AVAILABLE_PROMPTS.get((data_type, interface))
    if prompt is not None:
        return prompt(message, data_type)

    origin = typing.get_origin(data_type)
    if origin is not None:
        prompt = AVAILABLE_PROMPTS.get((origin, interface))
        if prompt is not None:
            return prompt(message, data_type)

    for cls in getattr(data_type, "__mro__", ()):
        if cls in (data_type, object):
            continue
        prompt = AVAILABLE_PROMPTS.get((cls, interface))
        if prompt is not None:
            return prompt(message, data_type)

    logger.error(f"No prompt found for type: {data_type}")
    return None
