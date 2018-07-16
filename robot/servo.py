"""Front-end servo board API."""
import enum
import functools
from typing import Any, Callable, Iterable, Optional

from robot.backends.base import BaseServoAssembly, ServoPosition


class CommandError(RuntimeError):
    """Error raised from a custom Arduino command."""

    pass


@enum.unique
class PinMode(enum.Enum):
    """GPIO pin mode."""

    INPUT = "input"
    INPUT_PULLUP = "input_pullup"
    OUTPUT_HIGH = "output_high"
    OUTPUT_LOW = "output_low"


class Servo:
    """An individual servo output on a servo board."""

    def __init__(
        self, *, drive: Callable[[float], None], initial_position: Optional[float]
    ) -> None:
        """
        Construct for internal use.

        Initialised from a started reporting position and a callable for setting new positions.
        """
        self._drive = drive
        self._position = initial_position

    @property
    def position(self) -> Optional[float]:
        """Get the current position to which this servo is driven."""
        return self._position

    @position.setter
    def position(self, new_position: Optional[float]) -> None:
        """Drive this servo to a new position."""
        self._position = new_position
        # We don't actually support setting to `None` alas
        if new_position is not None:
            self._drive(new_position)


class ServoBoard:
    """Front-end servo board."""

    def __init__(self, serial: str, backend: BaseServoAssembly) -> None:
        """Initialise with serial/backend."""
        self.serial = serial
        self._backend = backend

        self._num_servos = self._backend.num_servos()
        self._num_pins = self._backend.gpio_num_pins()

        self.servos = [
            Servo(drive=functools.partial(self._set_servo, n), initial_position=None)
            for n in range(self._backend.num_servos())
        ]

    def _set_servo(self, index: int, value: float) -> None:
        if value < -1.0 or value > 1.0:
            raise ValueError(
                "Servo ranges are from -1 to 1 (given: {value})".format(value=value)
            )
        mapped_value = int(value * 50.0 + 50.5)
        # Numerical edge cases
        if mapped_value < 0:
            mapped_value = 0
        elif mapped_value >= 100:
            mapped_value = 100
        self._backend.set_servo(index, ServoPosition(mapped_value))

    def direct_command(self, *args: Iterable[Any]) -> str:
        """
        Issue a command directly to the Arduino.

        The arguments are converted to strings and then encoded in UTF-8. The response is also
        decoded as UTF-8.

        In the event of an error response, `CommandError` is raised.
        """
        encoded_arguments = [str(x).encode("utf-8") for x in args]
        response = self._backend.direct_command(encoded_arguments)

        if response.error:
            raise CommandError(response.message.decode("utf-8"))

        return response.message.decode("utf-8")

    def read_ultrasound(self, output_pin: int, input_pin: int) -> float:
        """
        Send out an ultrasound ping.

        The ping is generated on `output_pin`, and we wait for an echo on `input_pin`. The time
        between transmit and receive is returned, in seconds.
        """
        self._validate_pin(output_pin)
        self._validate_pin(input_pin)
        return self._backend.ultrasound_pulse(output_pin, input_pin)

    def _validate_pin(self, pin: int) -> None:
        if pin < 0:
            raise ValueError(
                "Pin indices must be >= 0 (was given {pin})".format(pin=pin)
            )
        if pin > self._num_pins:
            raise ValueError(
                "Pin indices must be < {num_pins} (was given {pin})".format(
                    num_pins=self._num_pins, pin=pin
                )
            )
