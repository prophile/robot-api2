"""Dummy (testing) implementations of robot backends."""

from .motor import DummyMotorBoard, DummyMotorChannel
from .game_state import DummyGameState

__all__ = ["DummyMotorBoard", "DummyMotorChannel", "DummyGameState"]
