"""Test the Robot API Interface."""

import pytest

from robot import Robot, GameMode
from robot.power import PowerBoard
from robot.motor import MotorBoard
from robot.servo import ServoBoard
from robot.backends.base import BaseRobot
from robot.backends.dummy import (
    DummyRobot,
    DummyMotorChannel,
    DummyMotorBoard,
    DummyPowerBoard,
    DummyServoAssembly,
)


def _get_dummy_motor_board_backend():
    channels = [
        DummyMotorChannel()
        for _ in range(2)
    ]
    motor_board_backend = DummyMotorBoard(channels)
    return motor_board_backend


def _get_dummy_power_board_backend():
    power_board_backend = DummyPowerBoard()
    return power_board_backend


def _get_dummy_servo_assembly_backend():
    servo_assembly_backend = DummyServoAssembly()
    return servo_assembly_backend


def _get_dummy_robot():
    """
    Get an instance of robot with a dummy backend.

    Add some boards to make it work.
    
    """
    motor_boards = {
        "MTR0": _get_dummy_motor_board_backend(),
        "MTR1": _get_dummy_motor_board_backend(),
    }

    servo_assemblies = {
        "SRV0": _get_dummy_servo_assembly_backend(),
        "SRV1": _get_dummy_servo_assembly_backend(),
    }


    robot_backend = DummyRobot(
        motor_boards=motor_boards,
        power_boards={"PWR": _get_dummy_power_board_backend()},
        servo_assemblies=servo_assemblies,
    )
    
    return Robot(backend=robot_backend)


def test_get_default_backend():
    backend = Robot._get_default_backend()
    assert isinstance(backend, BaseRobot)


def test_initialisation():
    robot = _get_dummy_robot()
    
    assert type(robot.power_board) == PowerBoard

    assert len(robot.motor_boards) == 2
    assert type(robot.motor_boards["MTR0"]) == MotorBoard

    assert len(robot.servo_boards) == 2
    assert type(robot.servo_boards["SRV0"]) == ServoBoard


def test_initialisation_no_power_board():
    """We need to have a power board."""
    backend = DummyRobot(motor_boards={}, power_boards={}, servo_assemblies={})
    
    with pytest.raises(RuntimeError):
        robot = Robot(backend=backend)

def test_initialisation_no_backend():
    """
    If no backend is supplied, the default backend is selected.

    As the default backend currently has no PowerBoard, we should expect a RuntimeError.
    """
    with pytest.raises(RuntimeError):
        robot = Robot()


def test_initialisation_setups_backend():
    robot = _get_dummy_robot()

    assert robot._backend._setup_complete


def test_initialisation_waits_for_power():
    robot = _get_dummy_robot()

    assert robot.power_board._backend._waited_for_start


def test_no_power_button_wait():
    robot_backend = DummyRobot(
        motor_boards={},
        power_boards={"PWR": _get_dummy_power_board_backend()},
        servo_assemblies={},
    )

    robot = Robot(
        wait_for_start_button=False,
        backend=robot_backend,
    )

    assert not robot.power_board._backend._waited_for_start
    assert not robot.power_board._backend.outputs


def test_initialisation_too_many_power_boards():
    """We expect exactly one power board."""

    power_boards = {
        "PWR0": _get_dummy_power_board_backend(),
        "PWR1": _get_dummy_power_board_backend(),
    }

    backend = DummyRobot(
        motor_boards={},
        power_boards=power_boards,
        servo_assemblies={},
    )

    with pytest.raises(RuntimeError):
        robot = Robot(backend=backend)


def test_motor_board_getter_two_boards():
    """Firstly, test with two boards."""
    robot = _get_dummy_robot()

    with pytest.raises(RuntimeError):
        robot.motor_board


def test_motor_board_getter_one_board():
    """Test with one board. We should be able to use singular."""
    
    motor_boards = {
        "MTR0": _get_dummy_motor_board_backend(),
    }

    robot_backend = DummyRobot(
        motor_boards=motor_boards,
        power_boards={"PWR": _get_dummy_power_board_backend()},
        servo_assemblies={},
    )

    robot = Robot(backend=robot_backend)

    assert isinstance(robot.motor_board, MotorBoard)


def test_motor_board_getter_zero_boards():
    """Test with no motor boards."""

    robot_backend = DummyRobot(
        motor_boards={},
        power_boards={"PWR": _get_dummy_power_board_backend()},
        servo_assemblies={},
    )
    robot = Robot(backend=robot_backend)

    with pytest.raises(RuntimeError):
        robot.motor_board


def test_servo_board_getter_two_boards():
    """Test with two boards."""
    robot = _get_dummy_robot()

    with pytest.raises(RuntimeError):
        robot.servo_board


def test_servo_board_getter_one_board():
    """Test with one board. We should be able to use singular."""
    servo_assemblies = {
        "SRV0": _get_dummy_servo_assembly_backend(),
    }

    robot_backend = DummyRobot(
        motor_boards={},
        power_boards={"PWR": _get_dummy_power_board_backend()},
        servo_assemblies=servo_assemblies,
    )

    robot = Robot(backend=robot_backend)

    assert isinstance(robot.servo_board, ServoBoard)


def test_servo_board_getter_zero_boards():
    robot_backend = DummyRobot(
        motor_boards={},
        power_boards={"PWR": _get_dummy_power_board_backend()},
        servo_assemblies={},
    )
    robot = Robot(backend=robot_backend)

    with pytest.raises(RuntimeError):
        robot.servo_board


def test_robot_gamemode():
    """Test the gamemode attribute."""
    robot = _get_dummy_robot()

    assert robot.mode == GameMode.DEVELOPMENT


def test_robot_zone():
    """Test the zone attribute."""
    robot = _get_dummy_robot()

    assert robot.zone == 0