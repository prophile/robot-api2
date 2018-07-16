"""Central 'robot' class frontend definition."""
from typing import Optional

from robot.backends.base import BaseRobot
from robot.backends.dummy.robot import DummyRobot
from robot.motor import MotorBoard
from robot.power import PowerBoard


class Robot:
    """Main robot."""

    def __init__(
        self, *, wait_for_start_button: bool = True, backend: Optional[BaseRobot] = None
    ) -> None:
        """Initialise."""
        if backend is None:
            self._backend = self._get_default_backend()
        else:
            self._backend = backend

        self._backend.setup()

        power_boards = self._backend.power_boards()
        if len(power_boards) == 0:
            raise RuntimeError("There is no power board connected.")
        elif len(power_boards) > 1:
            raise RuntimeError("There are multiple power boards connected.")
        (power_board_serial, power_board_backend), = power_boards.items()
        self.power_board = PowerBoard(power_board_serial, power_board_backend)

        self.motor_boards = {
            serial: MotorBoard(serial, backend)
            for serial, backend in self._backend.motor_boards().items()
        }

        if wait_for_start_button:
            self.power_board.wait_start()

    @staticmethod
    def _get_default_backend() -> BaseRobot:
        return DummyRobot(motor_boards={}, power_boards={})

    @property
    def motor_board(self) -> MotorBoard:
        """Get the one motor board, if there is just one."""
        if not self.motor_boards:
            raise RuntimeError("There are no motor boards connected.")
        boards = list(self.motor_boards.values())
        if len(boards) > 0:
            raise RuntimeError(
                "There are multiple motor boards connected, use `.motor_boards`"
                "and index by serial number. Serial numbers: {serials}".format(
                    serials=", ".join(x.serial for x in boards)
                )
            )
        return boards[0]
