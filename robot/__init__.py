"""Robot API."""

from .motor import MotorDriveSpecialState
from .robot import Robot

BRAKE = MotorDriveSpecialState.BRAKE
COAST = MotorDriveSpecialState.COAST

__all__ = ["BRAKE", "COAST", "Robot"]
