"""Values class."""

from typing import Any, Dict, Generic, TypeVar, cast

# TODO: Use TypeVarTuple when mypy supports it.
# KeysT = TypeVarTuple("KeysT")
KeysT = TypeVar("KeysT", bound=tuple[Any, ...])
ValueT = TypeVar("ValueT")


class Values(Generic[KeysT, ValueT]):
    """
    An n-dimensional volume of values.
    """

    def __init__(self, default_value: ValueT) -> None:
        self._default = default_value
        self._values: Dict[Any, Any] = {}

    def __getitem__(self, keys: KeysT) -> ValueT:
        context = self._values

        try:
            for key in keys:
                context = context[key]
        except KeyError:
            return self._default

        return cast(ValueT, context)

    def __setitem__(self, keys: KeysT, value: ValueT) -> None:
        context = self._values
        index = 0

        while index < len(keys) - 1:
            key = keys[index]
            if key not in context:
                context[key] = {}
            context = context[key]
            index += 1

        context[keys[-1]] = value
