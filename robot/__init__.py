"""Robot API."""

from .motor import MotorDriveSpecialState

BRAKE = MotorDriveSpecialState.BRAKE
COAST = MotorDriveSpecialState.COAST

__all__ = ["BRAKE", "COAST"]
