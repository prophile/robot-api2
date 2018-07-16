"""Front-end motor board API."""
import enum
from typing import Union

from robot.backends.base import BaseMotorBoard, MotorPower


@enum.unique
class MotorDriveSpecialState(enum.Enum):
    """Special states for motor outputs."""

    BRAKE = "brake"
    COAST = "coast"


MotorDriveState = Union[MotorDriveSpecialState, float]


class MotorBoard(object):
    """Motor board."""

    def __init__(self, serial: str, backend: BaseMotorBoard) -> None:
        """Construct by serial/backend."""
        self.serial = serial
        self._backend = backend
        self._channels = {
            n: channel for n, channel in enumerate(self._backend.channels())
        }
        self._channel_states = {
            n: self._initial_channel_state() for n in self._channels.keys()
        }

    @classmethod
    def _initial_channel_state(cls) -> MotorDriveState:
        return MotorDriveSpecialState.COAST

    def _get_output(self, channel: int) -> MotorDriveState:
        return self._channel_states[channel]

    def _set_output(self, channel: int, state: MotorDriveState) -> None:
        self._channel_states[channel] = state
        backend_channel = self._channels[channel]
        if isinstance(state, float):
            if state >= 0.0:
                if state > 1.0:
                    raise ValueError(
                        "Cannot set motor output to >100% (we were told: {power})".format(
                            power=state
                        )
                    )
                backend_channel.forwards(MotorPower(state))
            else:
                if state < -1.0:
                    raise ValueError(
                        "Cannot set motor output to >100% (we were told: {power})".format(
                            power=state
                        )
                    )
                backend_channel.backwards(MotorPower(state))
        elif isinstance(state, MotorDriveSpecialState):
            if state is MotorDriveSpecialState.BRAKE:
                backend_channel.brake()
            elif state is MotorDriveSpecialState.COAST:
                backend_channel.forwards(MotorPower(0.0))
            else:
                raise AssertionError(
                    "Unknown enum value for drive state: {value}".format(value=state)
                )
        else:
            raise ValueError(
                "Didn't understand the value passed in: {value!r}".format(value=state)
            )

    @property
    def m0(self) -> MotorDriveState:
        """Motor channel 0 state."""
        return self._get_output(0)

    @m0.setter
    def m0(self, new_value: MotorDriveState) -> None:
        """Set motor channel 0 state."""
        self._set_output(0, new_value)

    @property
    def m1(self) -> MotorDriveState:
        """Motor channel 1 state."""
        return self._get_output(1)

    @m1.setter
    def m1(self, new_value: MotorDriveState) -> None:
        """Set motor channel 1 state."""
        self._set_output(1, new_value)
