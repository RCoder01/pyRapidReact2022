

class LikelyHardwareError(RuntimeWarning):
    """
    This exception is raised when a hardware error is detected.
    """
    pass


class SetpointOverrideWarning(RuntimeWarning):
    """
    This warning is raised when a read-only setpoint is attempted to be set.
    """
    pass
