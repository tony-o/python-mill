from collections import OrderedDict
from inspect import signature
from typing import Type

from .registry import get_type_generator


def factory(ignore_defaults: bool = False, ignore_mro: bool = False):
    def generator(cls: Type):
        _initfn = getattr(cls, "__init__")
        _signature = OrderedDict(signature(_initfn).parameters)
        _init_gens = {}
        _init_poss = {}
        _post_gens = {}
        minus = 0
        for idx, k in enumerate(_signature.keys()):
            if k == "self":
                minus = 1
                continue
            if _signature[k].default is not _signature[k].empty and not ignore_defaults:
                _init_gens[k] = (idx - minus, _signature[k].default)
            elif (
                _signature[k].annotation
                and _signature[k].annotation is not _signature[k].empty
            ):
                _init_gens[k] = (
                    idx - minus,
                    get_type_generator(_signature[k].annotation),
                )
            else:
                _init_gens[k] = (idx - minus, None)

            _init_poss[idx - minus] = k

        mro = [cls] if ignore_mro else cls.__mro__
        for obj in mro:
            for k, v in getattr(obj, "__annotations__", {}).items():
                if _init_gens.get(k, None) is not None:
                    continue
                _post_gens[k] = get_type_generator(v)

        def new(*args, **kwargs):
            sgrawk = {}
            for k, v in _init_gens.items():
                if (
                    kwargs.get(k, None) is None
                    and kwargs.get(k, 1) == 1
                    and v[0] >= len(args)
                ):
                    # not set in kwargs
                    sgrawk[k] = v[1]() if callable(v[1]) else v[1]
                elif len(args) > v[0]:
                    # not provided by args
                    sgrawk[k] = args[v[0]]
                else:
                    sgrawk[k] = kwargs[k]

            for idx, arg in enumerate(args):
                if _init_poss.get(idx, None):
                    k = _init_poss[idx]
                    sgrawk[k] = arg

            c = cls(**sgrawk)
            for k, v in _post_gens.items():
                setattr(c, k, v())

            return c

        return new

    return (
        generator
        if getattr(ignore_defaults, '__mro__', None) is None
        else generator(ignore_defaults)
    )
