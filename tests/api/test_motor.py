from robot import COAST, BRAKE
from robot.backends.dummy import DummyMotorChannel, DummyMotorBoard
from robot.motor import MotorBoard


def _get_dummy_motor_board():
    channels = [
        DummyMotorChannel()
        for _ in range(2)
    ]
    motor_board_backend = DummyMotorBoard(channels)
    motor_board_frontend = MotorBoard('SERIAL', motor_board_backend)
    return motor_board_frontend, motor_board_backend


def test_motor_channels_initialised_to_coast():
    dummy_board_frontend, dummy_board_backend = _get_dummy_motor_board()
    assert dummy_board_frontend.m0 == COAST
    assert dummy_board_frontend.m1 == COAST


def test_driving_forwards_on_m0():
    dummy_board_frontend, dummy_board_backend = _get_dummy_motor_board()
    dummy_board_frontend.m0 = 0.5
    assert dummy_board_backend.channels()[0].output == 0.5


def test_driving_forwards_then_coasting_on_m1():
    dummy_board_frontend, dummy_board_backend = _get_dummy_motor_board()
    dummy_board_frontend.m1 = 1.0
    dummy_board_frontend.m1 = COAST
    assert dummy_board_backend.channels()[1].output == 0.0


def test_braking_on_m1():
    dummy_board_frontend, dummy_board_backend = _get_dummy_motor_board()
    dummy_board_frontend.m1 = BRAKE
    assert dummy_board_backend.channels()[1].output is None
