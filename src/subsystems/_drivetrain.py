import commands2
import rev
import wpilib

import constants


class Drivetrain(commands2.SubsystemBase):

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber('Dirvetrain Left Encoder', self.get_left_encoder_position())
        wpilib.SmartDashboard.putNumber('Dirvetrain Right Encoder', self.get_right_encoder_position())
        super().periodic()
    
    def __init__(self) -> None:
        self._left_motors = [rev.CANSparkMax(ID, rev.CANSparkMaxLowLevel.MotorType.kBrushless) for ID in constants.DrivetrainConstants.LeftMotor.IDs]
        self._right_motors = [rev.CANSparkMax(ID, rev.CANSparkMaxLowLevel.MotorType.kBrushless) for ID in constants.DrivetrainConstants.RightMotor.IDs]

        for motor in self._left_motors[1:]:
            motor.follow(self._left_motors[0])
        
        for motor in self._right_motors[1:]:
            motor.follow(self._right_motors[0])
        
        self._left_lead_motor = self._left_motors[0]
        self._right_lead_motor = self._right_motors[0]

        self._left_lead_PID_controller = self._left_lead_motor.getPIDController()
        self._right_lead_PID_controller = self._right_lead_motor.getPIDController()

        super().__init__()
    
    def set_speed(self, left: float, right: float) -> None:
        """Sets the speed of the left and right motors."""
        self._left_lead_motor.set(left)
        self._right_lead_motor.set(right)
    
    def set_setpoints(self, left: float, right: float) -> None:
        """Sets integrated PID setpoints for the left and right motors."""
        self._left_lead_PID_controller.setReference(left, rev.CANSparkMax.ControlType.kPosition)
        self._right_lead_PID_controller.setReference(right, rev.CANSparkMax.ControlType.kPosition)
    
    def reset_encoders(self) -> None:
        """Resets the encoders.""" # TODO: Check if this resets reference frame or resets setpoint
        # TODO: Check if this is actually correct
        self._left_lead_motor.getEncoder().setPosition(0)
        self._right_lead_motor.getEncoder().setPosition(0)
    
    def get_left_encoder_position(self) -> float:
        """Returns the position of the drivetrain left encoder."""
        return self._left_lead_motor.getEncoder().getPosition()
    
    def get_right_encoder_position(self) -> float:
        """Returns the position of the drivetrain right encoder."""
        return self._right_lead_motor.getEncoder().getPosition()