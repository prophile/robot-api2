"""Front-end servo board API."""
from typing import Iterable, Any, Callable, Optional

from robot.backends.base import BaseServoAssembly


class CommandError(RuntimeError):
    pass


class Servo:
    """An individual servo output on a servo board."""

    def __init__(self, *, drive: Callable[[float], None], initial_position: Optional[float]):
        self._drive = drive
        self._position = initial_position

    @property
    def position(self) -> Optional[float]:
        return self._position

    @position.setter
    def position(self, new_position: Optional[float]) -> None:
        self._position = new_position
        self._drive(new_position)


class ServoBoard:
    """Front-end servo board."""

    def __init__(self, serial: str, backend: BaseServoAssembly) -> None:
        """Initialise with serial/backend."""
        self.serial = serial
        self._backend = backend

    def direct_command(self, *args: Iterable[Any]) -> str:
        encoded_arguments = [
            str(x).encode('utf-8')
            for x in args
        ]
        response = self._backend.direct_command(encoded_arguments)

        if response.error:
            raise CommandError(response.message.decode('utf-8'))

        return response.message.decode('utf-8')

    def read_ultrasound(self, output_pin: int, input_pin: int):
        self._validate_pin(output_pin)
        self._validate_pin(input_pin)
        return self._backend.ultrasound_pulse(output_pin, input_pin)
