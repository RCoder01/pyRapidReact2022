import commands2

import constants
import utils.motor


class Hub(commands2.SubsystemBase):
    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)
        self._motors = utils.motor.TalonFXGroup(constants.Climber.Hub.MOTOR_IDs)
        self._motors.configure_units(constants.Climber.Hub.ENCODER_COUNTS_PER_DEGREE)
    
    def set_position(self, angle: float):
        self._motors.set_configured_setpoint(angle)

    def get_position(self) -> float:
        return self._motors.get_configured_lead_encoder_position()
