"""Robot API."""

from .motor import MotorDriveState

BRAKE = MotorDriveState.BRAKE
COAST = MotorDriveState.COAST

__all__ = [
    'BRAKE',
    'COAST',
]
