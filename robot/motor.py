"""Front-end motor board API."""
import enum
from typing import Union

from robot.backends.base import BaseMotorBoard


@enum.unique
class MotorDriveSpecialState(enum.Enum):
    """Special states for motor outputs."""

    BRAKE = 'brake'
    COAST = 'coast'


MotorDriveState = Union[MotorDriveSpecialState, float]


class MotorBoard(object):
    """Motor board."""

    def __init__(self, serial: str, backend: BaseMotorBoard) -> None:
        """Construct by serial/backend."""
        self.serial = serial
        self._backend = backend
        self._channels = {
            n: channel
            for n, channel in enumerate(self._backend.channels())
        }
        self._channel_states = {
            n: MotorDriveSpecialState.COAST
            for n in self._channels.keys()
        }

    def _get_output(self, channel: int) -> MotorDriveState:
        return self._channel_states[channel]

    def _set_output(self, channel: int, state: MotorDriveState) -> None:
        pass

    @property
    def m0(self) -> MotorDriveState:
        return self._get_output(0)

    @m0.setter
    def m0(self, new_value: MotorDriveState) -> None:
        self._set_output(0, new_value)

    @property
    def m1(self) -> MotorDriveState:
        return self._get_output(1)

    @m1.setter
    def m1(self, new_value: MotorDriveState) -> None:
        self._set_output(1, new_value)
