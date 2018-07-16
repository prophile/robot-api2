"""Dummy (testing) implementations of robot backends."""

from .motor import DummyMotorBoard, DummyMotorChannel

__all__ = ["DummyMotorBoard", "DummyMotorChannel"]
