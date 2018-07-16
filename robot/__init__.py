"""Robot API."""

from robot.motor import MotorDriveSpecialState
from robot.robot import Robot
from robot.servo import CommandError

BRAKE = MotorDriveSpecialState.BRAKE
COAST = MotorDriveSpecialState.COAST

__all__ = ["BRAKE", "COAST", "Robot", "CommandError"]
