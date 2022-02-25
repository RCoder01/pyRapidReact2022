import wpilib
from commands2.button import Button, JoystickButton
import wpilib.interfaces

import utils.controls


_driver = wpilib.XboxController(0)
# _driver = wpilib.Joystick(0)
_manip = wpilib.XboxController(0)
# _manip = wpilib.Joystick(1)


class Drivetrain:
    class TankDrive:
        def get_left_speed() -> float:
            return utils.controls.deadzone(-_driver.getLeftY())

        def get_right_speed() -> float:
            return utils.controls.deadzone(-_driver.getRightY())

    class ArcadeDrive:
        def get_forward_speed() -> float:
            if _driver.getRightTriggerAxis() > 0:
                return _driver.getRightTriggerAxis()
            return -_driver.getLeftTriggerAxis()

        get_turn_speed = _driver.getLeftX


class Limelight:
    activate = JoystickButton(_driver, _driver.Button.kLeftBumper)
    # activate = JoystickButton(_driver, 0)


class Turret:
    manual_control = JoystickButton(_manip, _manip.Button.kA)
    turret_speed = _manip.getRightX


class Intake:
    activate = JoystickButton(_manip, _manip.Button.kB)
    # activate = JoystickButton(_manip, 2)


class Feeder:
    manual_activate = JoystickButton(_manip, _manip.Button.kY)


exgest = JoystickButton(_manip, _manip.Button.kX)
