"""Dummy implementations of motor board classes."""

from typing import Iterable, Optional, Sequence, cast

from robot.backends.base import BaseMotorBoard, BaseMotorChannel, MotorPower


class DummyMotorBoard(BaseMotorBoard):
    """Dummy (testing) implementation of a motor board."""

    def __init__(self, channels: Iterable[BaseMotorChannel]) -> None:
        """Construct from a manually-assembled iterable of channels."""
        self._channels = list(channels)

    def channels(self) -> Sequence[BaseMotorChannel]:
        """Get all the passed-in channels."""
        return self._channels


class DummyMotorChannel(BaseMotorChannel):
    """Dummy (testing) implementation of a motor board channel."""

    def __init__(self) -> None:
        """Construct with an initial freewheeling state."""
        self.output = self._initial_output()

    @classmethod
    def _initial_output(cls) -> Optional[float]:
        return 0.0

    def forwards(self, power: MotorPower) -> None:
        """Set output to the given power level, forwards."""
        self.output = cast(float, power)

    def backwards(self, power: MotorPower) -> None:
        """Set output to the given power level, backwards."""
        self.output = -cast(float, power)

    def brake(self) -> None:
        """Set output to the 'brake' state (i.e. None)."""
        self.output = None
