from enum import Enum
from mill.factory import factory


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class P:
    color: Color

    def __init__(self, color: Color = Color.GREEN):
        self.color = color


@factory()
class PDefaults(P):
    pass


@factory(ignore_defaults=True)
class PNoDefaults(P):
    pass


def test_default_works():
    assert PDefaults().color == Color.GREEN


def test_default_override():
    assert PDefaults(color=Color.RED).color == Color.RED


def test_positionals():
    assert PDefaults(Color.RED).color == Color.RED
