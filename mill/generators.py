import random
import string

from typing import Type

_data = {int: 0, str: 32}


def _str():
    return "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=_data[str],
        )
    )


def _int():
    _data[int] += 1
    return _data[int]


def _set_data(k: Type, v: any):
    _data[k] = v
