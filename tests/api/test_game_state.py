from robot import GameMode
from robot.backends.dummy import DummyGameState
from robot.game_state import GameState


def _get_dummy_game_state():

    game_state_backend = DummyGameState()
    game_state_frontend = GameState(game_state_backend)
    return game_state_frontend, game_state_backend


def test_gamestate_zone():
    game_state_frontend, game_state_backend = _get_dummy_game_state()
    assert game_state_frontend.zone == 0


def test_gamestate_mode():
    game_state_frontend, game_state_backend = _get_dummy_game_state()
    assert game_state_frontend.mode == GameMode.DEVELOPMENT
