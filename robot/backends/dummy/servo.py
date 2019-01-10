"""Dummy implementations of servo assembly classes."""

from typing import Iterable, Optional
from random import randint, getrandbits

from robot.backends.base import BaseServoAssembly, CommandResponse, ServoPosition


class DummyServoAssembly(BaseServoAssembly):
    """Dummy (testing) implementation of a servo assembly."""

    MODES = [
        "INPUT",
        "INPUT_PULLUP",
        "OUTPUT_LOW",
        "OUTPUT_HIGH",
    ]

    def __init__(self) -> None:
        """Initialise the state."""
        self._pins = [
            # Pin, State
            "INPUT" for n in range(0, 10)
        ]

        self._num_servos = 4

    def direct_command(self, args: Iterable[bytes]) -> CommandResponse:
        """
        Issue a direct, raw command.

        We are going to return the joined arguments.
        The error flag is set if the first byte is b'e'
        """
        data = b''.join(args)
        error_flag = data[0] == b'e'

        return CommandResponse(data, error_flag)

    def set_servo(self, servo: int, position: Optional[ServoPosition]) -> None:
        """Set a given servo to some specified position, including undriven."""
        if servo < 0 or servo >= self._num_servos:
            raise RuntimeError("That servo does not exist.")

    def ultrasound_pulse(self, out_pin: int, in_pin: int) -> float:
        """
        Trigger an ultrasound detection with a given input and output pin pair.

        The time delta is returned in seconds.
        """
        if self._pins[out_pin - 1].startswith("INPUT"):
            raise RuntimeError("The out pin is set as an input")

        if not self._pins[in_pin - 1].startswith("INPUT"):
            raise RuntimeError("The in pin is not set as an input")

        return randint(1, 1500) / 1000

    def gpio_output_high(self, pin: int) -> None:
        """Drive a given GPIO pin to high output."""
        self._pins[pin - 1] = "OUTPUT_HIGH"

    def gpio_output_low(self, pin: int) -> None:
        """Drive a given GPIO pin to low output."""
        self._pins[pin - 1] = "OUTPUT_LOW"

    def gpio_set_input(self, pin: int) -> None:
        """Set a given GPIO into high-impedance input mode."""
        self._pins[pin - 1] = "INPUT"

    def gpio_set_input_pullup(self, pin: int) -> None:
        """Set a given GPIO into pulled-up input mode."""
        self._pins[pin - 1] = "INPUT_PULLUP"

    def gpio_read_digital(self, pin: int) -> bool:
        """Read a digital value from a GPIO pin."""
        return bool(getrandbits(1))

    def gpio_can_read_analogue(self, pin: int) -> bool:
        """Check if a given GPIO can be used for ADC input."""
        return pin > 5

    def gpio_read_analogue(self, pin: int) -> float:
        """Read an analogue value, in volts, from a given GPIO pin."""
        return randint(0, 500) / 100

    def gpio_num_pins(self) -> int:
        """Get the number of available GPIO pins."""
        return len(self._pins)
