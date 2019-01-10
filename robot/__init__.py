"""Robot API."""

from robot.motor import MotorDriveSpecialState
from robot.robot import Robot
from robot.game_state import GameMode
from robot.servo import CommandError, PinMode, PinValue

BRAKE = MotorDriveSpecialState.BRAKE
COAST = MotorDriveSpecialState.COAST

__all__ = ["BRAKE", "COAST", "Robot", "CommandError", "PinMode", "PinValue", "GameMode"]
