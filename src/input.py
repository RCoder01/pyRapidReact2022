import wpilib
from commands2.button import Button, JoystickButton
import wpilib.interfaces


_driver = wpilib.XboxController(0)
# _driver = wpilib.Joystick(0)
# _manip = wpilib.XboxController(1)
_manip = wpilib.Joystick(1)


def get_tank_left_speed() -> float:
    return -_driver.getLeftY()
    # return _driver.getRawAxis(0)


def get_tank_right_speed() -> float:
    return -_driver.getRightY()
    # return _driver.getRawAxis(2)


def get_arcade_forward_speed() -> float:
    return _driver.getLeftY()


def get_arcade_turn_speed() -> float:
    return _driver.getRightX()


button_limelight_activate = JoystickButton(_driver, _driver.Button.kLeftBumper)
# button_limelight_activate = JoystickButton(_driver, 0)


def get_shooter_speed() -> float:
    # return _manip.getLeftTriggerAxis()
    return _manip.getRawAxis(1)


# get_shooter = JoystickButton(_manip, _manip.Button.kA)
get_shooter = JoystickButton(_manip, 1)


@Button
def get_shoot() -> bool:
    ...


# get_intake = JoystickButton(_manip, _manip.Button.kB)
get_intake = JoystickButton(_manip, 2)


@Button
def get_elevate() -> bool:
    ...


@Button
def get_climb() -> bool:
    ...
