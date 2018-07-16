"""Front-end power board API."""


class PowerBoard:
    """Front-end power board."""

    def __init__(self, serial: str) -> None:
        """Initialise with serial/backend."""
        self.serial = serial

    def wait_start(self) -> None:
        """Wait for the start button to be pressed."""
