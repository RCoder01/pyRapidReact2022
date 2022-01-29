import commands2
import ctre
import wpilib
import wpimath.controller

import constants


class Shooter(commands2.SubsystemBase):
    
    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber('Shooter Speed', self.get_jeff())

        self._current_jeff = self._pid_controller.calculate(self.get_jeff())
        self._lead_motor.set(ctre.ControlMode.PercentOutput, self._output)

        return super().periodic()
    
    # def simulationPeriodic(self) -> None:
    #     wpilib.SmartDashboard.putNumber('Shooter Motor Output', self._output)
    #     return super().simulationPeriodic()

    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)

        self._motors = [ctre.WPI_TalonFX(ID) for ID in constants.Shooter.IDs]
        self._lead_motor = self._motors[0]
        for motor in self._motors[1:]:
            motor.follow(self._lead_motor)

        self._pid_controller = wpimath.controller.PIDController(
            constants.Shooter.PID.P,
            constants.Shooter.PID.I,
            constants.Shooter.PID.D,
        )

        self._lead_sensor_collection = self._lead_motor.getSensorCollection()

        self._output = 0
    
    def set_jeff_setpoint(self, jeff: float) -> None:
        """Sets the speed of the shooter motors."""
        self._pid_controller.setSetpoint(jeff)
    
    def get_jeff_setpoint(self) -> float:
        """Returns the set speed of the shooter motor."""
        return self._pid_controller.getSetpoint()
    
    def get_jeff(self) -> float:
        """Returns the actual speed of the shooter motor."""
        return self._lead_sensor_collection.getIntegratedSensorVelocity()