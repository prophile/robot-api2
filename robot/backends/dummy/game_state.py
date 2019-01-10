"""Dummy (testing) game state implementation."""
from robot.backends.base import BaseGameState, GameMode


class DummyGameState(BaseGameState):
    """Testing game state."""

    def gamemode_read(self) -> GameMode:
        """Get the current game mode."""
        return GameMode.DEVELOPMENT

    def zone_read(self) -> int:
        """Get the current zone."""
        return 0
