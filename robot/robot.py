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

        self.power_board = PowerBoard("BEES")
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
