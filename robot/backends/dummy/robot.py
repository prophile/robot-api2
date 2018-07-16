"""Dummy robot implementation."""
from typing import Mapping

from robot.backends.base import BaseMotorBoard, BaseRobot


class DummyRobot(BaseRobot):
    """Dummy robot implementation."""

    def __init__(self, *, motor_boards: Mapping[str, BaseMotorBoard]) -> None:
        """Construct given pre-set dicts of boards."""
        self._motor_boards = dict(motor_boards)

    def setup(self) -> None:
        """Null setup."""
        pass

    def motor_boards(self) -> Mapping[str, BaseMotorBoard]:
        """Get all motor boards."""
        return self._motor_boards
