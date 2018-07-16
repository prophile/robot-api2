"""Base instances of robot backends."""

import abc
from typing import Iterable, Mapping, NewType, Optional, Sequence

MotorPower = NewType("MotorPower", float)
ServoPosition = NewType("ServoPosition", int)


class BaseMotorChannel(metaclass=abc.ABCMeta):
    """Abstract motor channel."""

    @abc.abstractmethod
    def forwards(self, power: MotorPower) -> None:
        """Drive the channel forwards with a given power."""
        raise NotImplementedError

    @abc.abstractmethod
    def backwards(self, power: MotorPower) -> None:
        """Drive the channel backwards with a given power."""
        raise NotImplementedError

    @abc.abstractmethod
    def brake(self) -> None:
        """Short the motor channels together."""
        raise NotImplementedError


class BaseMotorBoard(metaclass=abc.ABCMeta):
    """Abstract motor board implementation."""

    @abc.abstractmethod
    def channels(self) -> Sequence[BaseMotorChannel]:
        """Get all channels of this motor board."""
        raise NotImplementedError


class BasePowerBoard(metaclass=abc.ABCMeta):
    """Abstract power board implementation."""

    @abc.abstractmethod
    def enable_outputs(self) -> None:
        """Drive the main outputs to the battery voltage."""
        raise NotImplementedError

    @abc.abstractmethod
    def disable_outputs(self) -> None:
        """Drop the main outputs back to high-impedance."""
        raise NotImplementedError

    @abc.abstractmethod
    def wait_for_start_button(self) -> None:
        """Await the start button being pressed."""
        raise NotImplementedError


class CommandResponse(object):
    """A response to an Arduino command."""

    def __init__(self, message: bytes, error: bool) -> None:
        """Construct given whether an error, and a message."""
        self.message = message
        self.error = error

    def __repr__(self) -> str:
        """Reproducible representation."""
        return "{cls}(message={message!r}, error={error!r})".format(
            cls=type(self).__name__, message=self.message, error=self.error
        )


class BaseServoAssembly(metaclass=abc.ABCMeta):
    """Abstract servo assembly implementation."""

    @abc.abstractmethod
    def direct_command(self, args: Iterable[bytes]) -> CommandResponse:
        """Issue a direct, raw command."""
        raise NotImplementedError

    @abc.abstractmethod
    def num_servos(self) -> int:
        """Get the number of available servos."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_servo(self, servo: int, position: Optional[ServoPosition]) -> None:
        """Set a given servo to some specified position, including undriven."""
        raise NotImplementedError

    @abc.abstractmethod
    def ultrasound_pulse(self, out_pin: int, in_pin: int) -> float:
        """
        Trigger an ultrasound detection with a given input and output pin pair.

        The time delta is returned in seconds.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def gpio_output_high(self, pin: int) -> None:
        """Drive a given GPIO pin to high output."""
        raise NotImplementedError

    @abc.abstractmethod
    def gpio_output_low(self, pin: int) -> None:
        """Drive a given GPIO pin to high output."""
        raise NotImplementedError

    @abc.abstractmethod
    def gpio_set_input(self, pin: int) -> None:
        """Set a given GPIO into high-impedance input mode."""
        raise NotImplementedError

    @abc.abstractmethod
    def gpio_set_input_pullup(self, pin: int) -> None:
        """Set a given GPIO into pulled-up input mode."""
        raise NotImplementedError

    @abc.abstractmethod
    def gpio_read_digital(self, pin: int) -> bool:
        """Read a digital value from a GPIO pin."""
        raise NotImplementedError

    @abc.abstractmethod
    def gpio_read_analogue(self, pin: int) -> float:
        """Read an analogue value, in volts, from a given GPIO pin."""
        raise NotImplementedError

    @abc.abstractmethod
    def gpio_num_pins(self) -> int:
        """Get the number of available GPIO pins."""
        raise NotImplementedError


class BaseRobot(metaclass=abc.ABCMeta):
    """Abstract robot implementation."""

    @abc.abstractmethod
    def setup(self) -> None:
        """Make all connections and start running."""
        raise NotImplementedError

    @abc.abstractmethod
    def motor_boards(self) -> Mapping[str, BaseMotorBoard]:
        """Get motor boards by ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def power_boards(self) -> Mapping[str, BasePowerBoard]:
        """Get power boards by ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def servo_assemblies(self) -> Mapping[str, BaseServoAssembly]:
        """Get servo assemblies by ID."""
        raise NotImplementedError
