import builtins


class _Clamp:
    """
    Clamp with predefined min and max.
    """

    def __init__(self, min, max):
        self._min = min
        self._max = max

    def __call__(self, value):
        return clamp(self._min, self._max, value)


def clamp(value=None, min=-float('inf'), max=float('inf')):
    """
    Clamp a value between a min and max.

    If value is not provided, return an object with predefined limits that can be used to clamp multiple values.
    """

    if value is None:
        return _Clamp(min, max)

    return builtins.max(min, builtins.min(max, value))