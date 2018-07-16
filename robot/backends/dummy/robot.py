"""Dummy robot implementation."""
from typing import Mapping

from robot.backends.base import (
    BaseMotorBoard,
    BasePowerBoard,
    BaseRobot,
    BaseServoAssembly,
)


class DummyRobot(BaseRobot):
    """Dummy robot implementation."""

    def __init__(
        self,
        *,
        motor_boards: Mapping[str, BaseMotorBoard],
        power_boards: Mapping[str, BasePowerBoard],
        servo_assemblies: Mapping[str, BaseServoAssembly]
    ) -> None:
        """Construct given pre-set dicts of boards."""
        self._motor_boards = dict(motor_boards)
        self._power_boards = dict(power_boards)
        self._servo_assemblies = dict(servo_assemblies)

    def setup(self) -> None:
        """Null setup."""
        pass

    def motor_boards(self) -> Mapping[str, BaseMotorBoard]:
        """Get all motor boards."""
        return self._motor_boards

    def power_boards(self) -> Mapping[str, BasePowerBoard]:
        """Get all power boards."""
        return self._power_boards

    def servo_assemblies(self) -> Mapping[str, BaseServoAssembly]:
        """Get all servo assemblies."""
        return self._servo_assemblies
