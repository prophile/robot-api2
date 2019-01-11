"""Dummy (testing) power board implementation."""
from robot.backends.base import BasePowerBoard


class DummyPowerBoard(BasePowerBoard):
    """Testing power board."""

    def __init__(self) -> None:
        """Initialise, with outputs disabled."""
        self.outputs = False
        self._waited_for_start = False

    def enable_outputs(self) -> None:
        """Drive the outputs to high."""
        self.outputs = True

    def disable_outputs(self) -> None:
        """Stop driving the outputs."""
        self.outputs = False

    def wait_for_start_button(self) -> None:
        """Mark as waited for testing."""
        self._waited_for_start = True
