from aioalice.utils import exceptions
from aioalice.utils.json import json
from aioalice.utils.payload import generate_json_payload
from aioalice.utils.safe_kwargs import safe_kwargs


def ensure_cls(*classes):
    from aioalice.types.base import AliceObject

    safe_classes = [safe_kwargs(cls) if issubclass(cls, AliceObject) else cls for cls in classes]

    def converter(val):
        if val is None:
            return
        if isinstance(val, dict):
            for cls in safe_classes:
                try:
                    return cls(**val)
                except TypeError:
                    pass
        if isinstance(val, list):
            return [converter(v) for v in val]
        for cls in classes:
            if not isinstance(val, cls):
                try:
                    return cls(val)
                except TypeError:
                    pass
        return val

    return converter


__all__ = [
    "exceptions",
    "json",
    "generate_json_payload",
    "safe_kwargs",
    "ensure_cls",
]
