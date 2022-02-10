import math
import typing
import wpilib
import commands2
import ctre

class HeadedDefaultMotorGroup:

    # ENCODER_COUNTS_PER_ROTATION: int = constansts.Misc.ENCODER_COUNTS_PER_ROTATION

    def __init__(self, ID_List: typing.Collection[int], encoder_counts_per_rotation: int = None, inversions: typing.Collection[bool] = None) -> None:
        self.motors = [ctre.WPI_TalonFX(ID) for ID in ID_List]
        self.lead = self.motors[0]
        for motor in self.motors[1:]:
            motor.follow(self.lead)

        if inversions is None:
            for motor in self.motors[1:]:
                motor.setInverted(ctre.InvertType.FollowMaster)
        else:
            for motor, inverted in zip(self.motors, inversions):
                if inverted:
                    motor.setInverted(ctre.InvertType.FollowMaster)
                else:
                    motor.setInverted(ctre.InvertType.OpposeMaster)

        if encoder_counts_per_rotation is not None:
            self.ENCODER_COUNTS_PER_ROTATION = encoder_counts_per_rotation

    def get_lead_encoder_position(self):
        """Return the encoder position of the lead motor."""
        return self.lead.getSelectedSensorPosition() or 0

    def get_lead_encoder_velocity(self):
        """Return the encoder velocity of the lead motor."""
        return self.lead.getSelectedSensorVelocity() or 0

    def reset_lead_encoder(self):
        """Reset the encoder of the lead motor."""
        self.lead.setSelectedSensorPosition(0)

    def invert_all(self, inverted: bool = True):
        """Set the inversion of the motors."""
        self.lead.setInverted(inverted)

    def set_netural_mode_coast(self):
        """Set the motors so that tey coast when neutral."""
        self.lead.setNeutralMode(ctre.NeutralMode.Coast)
        for motor in self.motors:
            motor.setNeutralMode(ctre.NeutralMode.Coast)

    def set_netural_mode_brake(self):
        """Set the motors so that they brake when neutral."""
        self.lead.setNeutralMode(ctre.NeutralMode.Brake)
        for motor in self.motors:
            motor.setNeutralMode(ctre.NeutralMode.Brake)

    def set_output(self, value: float):
        """
        Set the speed of the motors, using the default configuration.

        :param value: The speed to set the motors to, ranging from -1 to 1.
        """
        self.lead.set(ctre.ControlMode.PercentOutput, value)

    def set_velocity(self, target_velocity: float):
        """Set the velocity of the motors, using the default configuration."""
        self.lead.set(ctre.ControlMode.Velocity, target_velocity)
def deadzone(
        input,
        power=2,
        lower_maxzone=-1,
        lower_deadzone=-0.1,
        higher_deadzone=0.1,
        higher_maxzone=1,
        ):
    """
    Highly customizable deadzone function, 
    Follows equations at https://www.desmos.com/calculator/yt5brsfh1m

    :param input:
    The value to be set into deadzone
    :param power:
    The power to which the function should be taken;
    1 is linear, 2 is quadratic, etc.
    :param lower_maxzone:
    The negative point past which all inputs return -1
    :param lower_deadzone:
    The negative point past which all less inputs return 0
    :param higher_deadzone:
    The positive point past which all less inputs return 0
    :param higher_maxzone:
    The positive point at which all past inputs return 1

    :returns:
    Input modified by the different parameters

    Values must follow:
    -1 <= lower_maxzone < lower_deadzone <= 0
    <= higher_deadzone < higher_maxzone <= 1
    or ValueError will be raised
    """
    if not(
        -1 <= lower_maxzone < lower_deadzone <= 0
        <= higher_deadzone < higher_maxzone <= 1
    ):
        raise ValueError(
            'The following must be true: '
            '-1 <= lower_maxzone < lower_deadzone <= 0'
            '<= higher_deadzone < higher_maxzone <= 1'
        )
    if not(power >= 0):
        raise ValueError('Power must be greater than or equal to zero')

    # Depedning on range, use a different output formula
    if input <= lower_maxzone:
        return -1
    if lower_maxzone < input < lower_deadzone:
        return -math.pow(
            (-input + lower_deadzone) / (lower_deadzone - lower_maxzone),
            power,
        )
    if lower_deadzone <= input <= higher_deadzone:
        return 0
    if higher_deadzone < input < higher_maxzone:
        return math.pow(
            (input - higher_deadzone) / (higher_maxzone - higher_deadzone),
            power,
        )
    if higher_maxzone <= input:
        return 1


class Drivetrain(commands2.SubsystemBase):
    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)
        self.left_motors = HeadedDefaultMotorGroup([1, 3])
        self.right_motors = HeadedDefaultMotorGroup([2, 4])
        self.left_motors.invert_all()
    
    def set_speeds(self, left: float, right: float):
        self.left_motors.set_output(left)
        self.right_motors.set_output(right)

drivetrain = Drivetrain()

class TankDrive(commands2.CommandBase):
    def __init__(self, left_power_supplier, right_power_supplier) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(drivetrain)
        self.setName('Tank Drive')
        self._left_power_supplier = left_power_supplier
        self._right_power_supplier = right_power_supplier

    def execute(self) -> None:
        drivetrain.set_speeds(self._left_power_supplier(), self._right_power_supplier())
        return super().execute()

class Robot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        # self.controller = wpilib.XboxController(0)
        return super().robotInit()
    
    def teleopInit(self) -> None:
        # drivetrain.setDefaultCommand(TankDrive(
        #     (lambda: deadzone(self.controller.getLeftY()) * -1),
        #     (lambda: deadzone(self.controller.getRightY())
        # )))
        self.m = [ctre.WPI_TalonFX(i) for i in [1, 2, 3, 4]]
        for m in self.m:
            m.set(0.1)
        return super().teleopInit()

    def teleopPeriodic(self) -> None:
        # return super().teleopPeriodic()
        pass

if __name__ == '__main__':
    wpilib.run(Robot)
