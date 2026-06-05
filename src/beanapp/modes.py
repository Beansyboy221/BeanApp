"""A framework for dynamically loaded program modes."""

import importlib
import logging
import typing

import pydantic

logger = logging.getLogger("BeanApp Modes")


class ProgramMode:
    """A manifest for registering and running program modes."""

    def __init__(
        self,
        name: str,
        description: str,
        config_class: type[pydantic.BaseModel],
        entry_point: str,
    ):
        self.name = name
        self.description = description
        self.config_class = config_class
        self.entry_point = entry_point
        AVAILABLE_MODES[self.name] = self

    def run(self, raw_config: dict) -> typing.Any:
        """Imports and runs the entry point."""
        logger.info(f"Running mode: {self.name}")
        module = importlib.import_module(self.entry_point)
        return module.main(self.config_class.model_validate(raw_config))


AVAILABLE_MODES: dict[str, ProgramMode] = {}
"""
A registry of all loaded modes.\n
Key: the mode's name\n
Value: the mode instance
"""
