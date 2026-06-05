"""Test mode config for ProgramMode.run()."""

import pydantic


class TestModeConfig(pydantic.BaseModel):
    value: str
