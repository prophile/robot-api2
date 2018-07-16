"""Base instances of robot backends."""

import abc
from typing import NewType, Sequence

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
