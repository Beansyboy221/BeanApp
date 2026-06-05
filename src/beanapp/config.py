"""Configs for app startup."""

import enum

import pydantic_settings
import pydantic

from . import modes


class LogLevel(enum.StrEnum):
    """Config selectable log levels for the logging module"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"


class StartupConfig(pydantic_settings.BaseSettings, cli_parse_args=True):
    """
    Settings for app startup.
    Tries to load config from environment clargs first.
    """

    mode: modes.ProgramMode = pydantic.Field(description="The mode to be run in main.")
    """The mode to be run in main."""

    log_level: LogLevel = pydantic.Field(
        default=LogLevel.INFO, description="The severity level of the main logger."
    )
    """The severity level of the main logger."""

    config_path: pydantic.FilePath | None = pydantic.Field(
        default=None, description="The path to your app config file."
    )
    """The path to your app config file."""

    log_path: pydantic.DirectoryPath | None = pydantic.Field(
        default=None, description="Path to write log output to."
    )
    """Path to write log output to."""

    locale: str = pydantic.Field(
        default="en-us", description="The language for the application."
    )
    """The language for the application."""
