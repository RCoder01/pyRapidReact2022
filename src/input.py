import wpilib
from commands2.button import Button, JoystickButton
import wpilib.interfaces


_driver = wpilib.XboxController(0)
_manip = wpilib.XboxController(1)


def get_tank_left_speed() -> float:
    return -_driver.getLeftY()


def get_tank_right_speed() -> float:
    return -_driver.getRightY()


def get_arcade_forward_speed() -> float:
    return _driver.getLeftY()


def get_arcade_turn_speed() -> float:
    return _driver.getRightX()


button_limelight_activate = JoystickButton(_driver, _driver.Button.kLeftBumper)


@Button
def get_shoot() -> bool:
    ...


@Button
def get_intake() -> bool:
    return _driver.getBButton()


@Button
def get_elevate() -> bool:
    ...


@Button
def get_climb() -> bool:
    ...