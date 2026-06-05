"""A framework for manual and automatic user prompting."""

import sys

from . import api  # noqa: F401
from .prompts import cli
from .prompts.cli import beanapp as cli_beanapp  # noqa: F401
from .prompts.cli import builtins as cli_builtins  # noqa: F401
from .prompts.cli import pydantic as cli_pydantic  # noqa: F401
from .prompts.cli import typing as cli_typing  # noqa: F401

sys.modules[__name__ + ".cli"] = cli

try:
    from .prompts import tk
    from .prompts.tk import beanapp as tk_beanapp  # noqa: F401
    from .prompts.tk import builtins as tk_builtins  # noqa: F401
    from .prompts.tk import pydantic as tk_pydantic  # noqa: F401
    from .prompts.tk import typing as tk_typing  # noqa: F401

    sys.modules[__name__ + ".tk"] = tk
except ImportError:
    pass
