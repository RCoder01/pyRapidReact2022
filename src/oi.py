import wpilib
from commands2.button import Button, JoystickButton
import wpilib.interfaces
import utils.controls


_driver = wpilib.XboxController(0)
# _driver = wpilib.Joystick(0)
_manip = wpilib.XboxController(1)
# _manip = wpilib.Joystick(1)


def get_tank_left_speed() -> float:
    return utils.controls.deadzone(-_driver.getLeftY())


def get_tank_right_speed() -> float:
    return utils.controls.deadzone(-_driver.getRightY())


def get_arcade_forward_speed() -> float:
    if _driver.getLeftTriggerAxis() > 0:
        return _driver.getLeftTriggerAxis()
    return -_driver.getRightTriggerAxis()


def get_arcade_turn_speed() -> float:
    return _driver.getLeftX()


button_limelight_activate = JoystickButton(_driver, _driver.Button.kLeftBumper)
# button_limelight_activate = JoystickButton(_driver, 0)


turret_manual_control = JoystickButton(_manip, _manip.Button.kA)


# get_shooter = JoystickButton(_manip, _manip.Button.kA)
get_shooter = JoystickButton(_manip, 1)


@Button
def get_shoot() -> bool:
    ...


get_intake = JoystickButton(_driver, _driver.Button.kB)
# get_intake = JoystickButton(_manip, 2)


@Button
def get_elevate() -> bool:
    ...


@Button
def get_climb() -> bool:
    ...
