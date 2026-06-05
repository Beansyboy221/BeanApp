"""Example mode package for testing."""

from src.beanapp import ProgramMode
from . import config

mode2 = ProgramMode(
    name="mode2",
    description="Second test mode",
    config_class=config.TestModeConfig,
    entry_point="tests.test_modes.modes.mode2.main",
)
