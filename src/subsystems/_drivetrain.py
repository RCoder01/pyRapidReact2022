import commands2
import ctre
import wpilib

import constants


class Drivetrain(commands2.SubsystemBase):

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber('Dirvetrain Left Encoder', self.get_left_encoder_position())
        wpilib.SmartDashboard.putNumber('Dirvetrain Right Encoder', self.get_right_encoder_position())

        return super().periodic()
    
    def simulationPeriodic(self) -> None:
        wpilib.SmartDashboard.putNumber('Drivetrain Left Motor Output', self._left_speed)
        wpilib.SmartDashboard.putNumber('Drivetrain Right Motor Output', self._right_speed)

        return super().simulationPeriodic()
    
    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)

        self._left_motors = [ctre.WPI_TalonFX(ID) for ID in constants.Drivetrain.LeftMotor.IDs]
        self._right_motors = [ctre.TalonFX(ID) for ID in constants.Drivetrain.RightMotor.IDs]

        for motor in self._left_motors[1:]:
            motor.follow(self._left_motors[0])
        
        for motor in self._right_motors[1:]:
            motor.follow(self._right_motors[0])
        
        self._left_lead_motor = self._left_motors[0]
        self._right_lead_motor = self._right_motors[0]

        self._left_lead_motor_sensor_collection = self._left_lead_motor.getSensorCollection()
        self._right_lead_motor_sensor_collection = self._right_lead_motor.getSensorCollection()

        self._left_speed = 0
        self._right_speed = 0
    
    def set_speed(self, left: float, right: float) -> None:
        """Sets the speed of the left and right motors."""
        self._left_speed = left
        self._right_speed = right

        self._left_lead_motor.set(ctre.ControlMode.PercentOutput, left)
        self._right_lead_motor.set(ctre.ControlMode.PercentOutput, right)
    
    def get_left_encoder_position(self) -> float:
        """Returns the position of the drivetrain left encoder."""
        return self._left_lead_motor_sensor_collection.getIntegratedSensorPosition()
    
    def get_right_encoder_position(self) -> float:
        """Returns the position of the drivetrain right encoder."""
        return self._right_lead_motor_sensor_collection.getIntegratedSensorPosition()