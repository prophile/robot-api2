"""Front-end game state API."""
from robot.backends.base import BaseGameState, GameMode


class GameState:
    """Front-end game state."""

    def __init__(self, backend: BaseGameState) -> None:
        """Initialise with backend."""
        self._backend = backend

    @property
    def zone(self) -> int:
        """Get the zone."""
        return self._backend.zone_read()

    @property
    def mode(self) -> GameMode:
        """Get the current game mode."""
        return self._backend.gamemode_read()
