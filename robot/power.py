"""Front-end power board API."""
from robot.backends.base import BasePowerBoard


class PowerBoard:
    """Front-end power board."""

    def __init__(self, serial: str, backend: BasePowerBoard) -> None:
        """Initialise with serial/backend."""
        self.serial = serial
        self._backend = backend
        self._backend.disable_outputs()

    def wait_start(self) -> None:
        """Wait for the start button to be pressed."""
        self._backend.wait_for_start_button()
        self._backend.enable_outputs()
