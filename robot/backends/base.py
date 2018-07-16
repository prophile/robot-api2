"""Base instances of robot backends."""

import abc
from typing import Mapping, NewType, Sequence

MotorPower = NewType("MotorPower", float)


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
