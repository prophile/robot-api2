"""Test the motor board frontend."""
from robot.backends.dummy import DummyPowerBoard
from robot.power import PowerBoard

def _get_dummy_power_board():
    power_board_backend = DummyPowerBoard()
    power_board_frontend = PowerBoard("SERIAL", power_board_backend)
    return power_board_frontend, power_board_backend

def test_outputs_initialised_to_disabled():
    power_board_frontend, power_board_backend = _get_dummy_power_board()
    # TODO: This is too specific to the dummy backend. 
    # We probably need a output_state function.
    assert not power_board_backend.outputs

def test_outputs_enabled_after_start():
    power_board_frontend, power_board_backend = _get_dummy_power_board()
    power_board_frontend.wait_start()
    # TODO: This is too specific to the dummy backend. 
    # We probably need a output_state function.
    assert power_board_backend.outputs
