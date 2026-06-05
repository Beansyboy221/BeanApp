"""Tests for beanapp.modes."""

from src.beanapp import modes

from .modes import mode1, mode2


class TestDynamicLoading:
    def test_all_modes_register(self):
        assert "mode1" in modes.AVAILABLE_MODES
        assert "mode2" in modes.AVAILABLE_MODES

    def test_run_each_mode(self):
        for name, expected in [
            ("mode1", "ran with hello"),
            ("mode2", "ran with world"),
        ]:
            mode = modes.AVAILABLE_MODES[name]
            result = mode.run({"value": expected.split()[-1]})
            assert result == expected
