"""CLI prompts for BeanApp types."""

from ...api import register
from .... import config, modes

from . import builtins


@register(config.LogLevel)
def prompt_log_level(
    message: str = f"Please input a log level ({', '.join(config.LogLevel.__members__)}).",
    data_type: type = config.LogLevel,
) -> str:
    while True:
        try:
            return config.LogLevel(builtins.prompt_str(message))
        except ValueError:
            print(
                f"Invalid input. Enter one of the following: {config.LogLevel.__members__}"
            )


@register(modes.ProgramMode)
def prompt_program_mode(
    message: str = "Select a program mode.",
    data_type: type = modes.ProgramMode,
) -> modes.ProgramMode:
    if not modes.AVAILABLE_MODES:
        raise ValueError("No modes available.")
    options = list(modes.AVAILABLE_MODES.values())
    print(f"\n{message}")
    for index, mode in enumerate(options, start=1):
        print(f"  [{index}] {mode.name} - {mode.description}")
    while True:
        choice = input("Enter the index of the mode: ").strip()
        try:
            return options[int(choice) - 1]
        except (ValueError, IndexError):
            print(f"Invalid choice. Choose a number between 1 and {len(options)}.")
