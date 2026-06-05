"""Entry point for RunTestMode."""

from . import config


def main(config: config.TestModeConfig):
    return f"ran with {config.value}"
