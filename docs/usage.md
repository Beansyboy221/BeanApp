# BeanApp Usage Guide

## Global App Configuration

The [`StartupConfig`](../src/beanapp/config.py) model provides basic settings many desktop apps use. It parses CLI args automatically via `pydantic-settings` and can be subclassed to add your own fields.

Included Fields:

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| `mode` | `beanapp.modes.ProgramMode` | *(required)* | The mode to run in `main()` |
| `log_level` | `beanapp.config.LogLevel` | `INFO` | Severity threshold for the root logger |
| `config_path` | `pydantic.FilePath or None` | `None` | Path to your app config file |
| `log_path` | `pydantic.DirectoryPath or None` | `None` | Directory to write log files |
| `locale` | `str` | `"en-us"` | Language / locale for the application |

`LogLevel` is a `StrEnum` with: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`, `FATAL`.

Example:

```python
# myapp/main.py
from beanapp import StartupConfig
from pydantic import Field

class MyConfig(StartupConfig):
    window_size: tuple[int, int] = Field(default=(1024, 768))
    theme: str = Field(default="dark")

config = MyConfig() # parses CLI args used to launch the program
```

## Program Modes

The [`modes`](../src/beanapp/modes.py) module can be used to organize your app into modes that register when instantiated and can be loaded and run lazily:

```python
# myapp/modes/my_mode/__init__.py
from beanapp import ProgramMode

my_mode = ProgramMode(
    name="my_mode",
    description="Does something useful",
    config_class=MyConfig,
    entry_point="myapp.modes.my_mode.main",
)  # registers in AVAILABLE_MODES

# myapp/modes/my_mode/config.py
from pydantic import BaseModel

class MyConfig(BaseModel):
    name: str

# myapp/modes/my_mode/main.py
from .config import MyConfig

def main(config: MyConfig):
    print(f"Running with name: {config.name}")
```

When `run(raw_config: dict)` is called, it dynamically imports the module given by `entry_point` and calls its pathed function like so: `main(MyConfig.model_validate(raw_config))`

## User Prompting

The [`prompt api`](../src/beanapp/modes.py) can be used to prompt the user for values dynamically. You can also manually import prompts.

### Dynamic Dispatch

`prompt()` looks up the right prompt by `(type, interface)` and calls it. If no exact match is found, it first checks the type's generic origin (e.g. `list[int]` → `list`), then walks the MRO to find a registered ancestor prompt. This lets concrete Pydantic models fall back to a `BaseModel` prompt automatically.

```python
from beanapp import prompt

# CLI (default interface)
name = prompt(str, "Enter your name:")
age = prompt(int, "Enter your age:")
level = prompt(LogLevel, "Select log level:")
config = prompt(MyConfig, "Configure the app:")  # uses BaseModel prompt via MRO

# Tkinter
name = prompt(str, "Enter your name:", interface="tk")
```

### Direct Import

You can easily skip the dispatcher and call a prompt directly. This is useful when you know exactly what you need:

```python
from beanapp.prompting.cli.builtins import prompt_str, prompt_int
from beanapp.prompting.cli.pydantic import prompt_file_path, prompt_pydantic_model
from beanapp.prompting.tk.builtins import prompt_str as tk_str

name = prompt_str("Enter your name:", str)
age = prompt_int("Enter your age:", int)
path = prompt_file_path("Enter config path:", None)
config = prompt_pydantic_model("Configure:", MyConfig)
name = tk_str("Enter your name:", str)
```

### Included Prompts

BeanApp comes with some basic prompts that use both a CLI (prompting.prompts.cli) and Tkinter dialogs (prompting.prompts.tk):

| Prompt | Type | CLI | TK |
| -------- | ---- | --- | -- |
| `prompt_str` | `str` | Free text | `simpledialog.askstring` |
| `prompt_int` | `int` | Whole number (e.g., `42`) | `simpledialog.askinteger` |
| `prompt_float` | `float` | Decimal or integer (e.g., `3.14`) | `simpledialog.askfloat` |
| `prompt_complex` | `complex` | Complex number (e.g., `1+2j`) | `simpledialog.askstring` + validation |
| `prompt_bool` | `bool` | `true/false`, `t/f`, `yes/no`, `y/n`, `1/0` | `messagebox.askyesno` |
| `prompt_list` | `list` | Space-separated or element-by-element | `ScrolledTextDialog` or element-by-element |
| `prompt_tuple` | `tuple` | Element-by-element with type selection | `ScrolledTextDialog` or `ListboxDialog` |
| `prompt_set` | `set` | Space-separated or element-by-element | `ScrolledTextDialog` or element-by-element |
| `prompt_frozenset` | `frozenset` | Space-separated or element-by-element | `ScrolledTextDialog` or element-by-element |
| `prompt_dict` | `dict` | Comma-separated `key=value` or key/value prompting | `ScrolledTextDialog` with `key=value` lines or key/value prompting |
| `prompt_union` | `types.UnionType` | Select from union members | `ListboxDialog` to select member type |
| `prompt_log_level` | `LogLevel` | Log level name (e.g., `INFO`) | `ComboboxDialog` dropdown |
| `prompt_program_mode` | `ProgramMode` | Select from available modes by index | `ListboxDialog` with mode names |
| `prompt_file_path` | `pydantic.FilePath` | Valid file path (validated by Pydantic) | `filedialog.askopenfilename` + Pydantic validation |
| `prompt_directory_path` | `pydantic.DirectoryPath` | Valid directory path (validated by Pydantic) | `filedialog.askdirectory` + Pydantic validation |
| `prompt_pydantic_model` | `pydantic.BaseModel` | Iterates model fields, prompts for each by annotation | Iterates model fields, prompts for each by annotation via `prompt(interface="tk")` |

### Custom Prompts

Register a prompt for any type so `prompt()` can find it:

```python
# myapp/prompts/cli/pydantic.py
import pydantic

from beanapp import register, prompt
from beanapp.prompting.cli.builtins import prompt_str

@register(pydantic.PositiveInt)
def prompt_positive_int(
    message="Enter a positive whole number.", data_type: type = pydantic.PositiveInt
) -> pydantic.PositiveInt:
    adapter = pydantic.TypeAdapter(data_type)
    while True:
        try:
            return adapter.validate_python(prompt_str(message))
        except pydantic.ValidationError:
            print("Invalid input. Enter a positive integer.")

```

Custom prompts should always have only two input args: `message:str` and `data_type:type`. It is also recommended that you set a default for both and hint the return type of the prompt for direct usage.

All validation should live in the `data_type`, not the prompt. The prompt's only job is to collect and convert raw input to the output type. This keeps prompts generic and reusable.

Annotated types are not currently unpacked by the prompting api and must have explicitly implemented prompts. This is because the api cannot predict the purpose of the annotated metadata.

### Custom Dialogs

BeanApp includes some convenient Tkinter dialogs you can use directly inside custom prompts or standalone in your app. Each extends `tkinter.simpledialog.Dialog` and stores its result in `self.result`.

The pattern is the same for all dialogs. Here is an example using `SelectDialog`:

```python
from beanapp.prompting.dialogs.selectdialog import SelectDialog

print(SelectDialog(
    title="Select Fruit", 
    prompt="Choose one:", 
    items=["Apple", "Banana", "Cherry"]
).result)
```

All available dialogs:

| Dialog | Purpose | Constructor Parameters | Returns |
| ------- | ------- | ---------------------- | ------- |
| `SelectDialog` | Selection from a scrollable list | `title: str, prompt: str, items: typing.Sequence, multiselect: bool = False, parent=None` | Single selected item or a list of selected items |
| `ScrolledTextDialog` | Enter or edit multi-line text | `title: str, prompt: str, initial_text: str = "", parent=None` | String contents |
