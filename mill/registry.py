import random

from enum import Enum
from typing import Callable, Type

from .generators import _int, _str

registry = {
    int: _int,
    str: _str,
}


class TypeNotFoundException(Exception):
    pass


def get_type_generator(s: Type):
    if issubclass(s, Enum):
        return lambda: random.choice(list(s))
    if not registry.get(s):
        raise TypeNotFoundException(
            f"Type ({s}) not found in registry.  Try importing and calling mill.registry.set_type_generator with the type/Callable desired"
        )
    return registry[s]


def set_type_generator(s: Type, n: Callable):
    registry[s] = n
