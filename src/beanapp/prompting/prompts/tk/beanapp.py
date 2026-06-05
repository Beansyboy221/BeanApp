"""TK prompts for BeanApp types."""

import tkinter.messagebox

from ...api import register
from ...dialogs import SelectDialog
from .... import config, modes


@register(config.LogLevel, interface="tk")
def prompt_log_level(
    message: str = "Select a log level.",
    data_type: type = config.LogLevel,
) -> config.LogLevel:
    result = SelectDialog(
        title="Input",
        prompt=message,
        items=list(config.LogLevel.__members__),
    ).result
    return config.LogLevel(result)


@register(modes.ProgramMode, interface="tk")
def prompt_program_mode(
    message: str = "Select a program mode.",
    data_type: type = modes.ProgramMode,
) -> modes.ProgramMode:
    if not modes.AVAILABLE_MODES:
        raise ValueError("No modes available.")
    display_items = [
        f"{mode.name} - {mode.description}" for mode in modes.AVAILABLE_MODES.values()
    ]
    while True:
        result = SelectDialog("Input", message, display_items).result
        if result is not None:
            index = display_items.index(result)
            return list(modes.AVAILABLE_MODES.values())[index]
        tkinter.messagebox.showerror("Cannot select nothing. Please try again.")
