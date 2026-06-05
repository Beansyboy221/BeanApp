"""Example mode package for testing."""

from src.beanapp import ProgramMode
from . import config

mode1 = ProgramMode(
    name="mode1",
    description="First test mode",
    config_class=config.TestModeConfig,
    entry_point="tests.test_modes.modes.mode1.main",
)
