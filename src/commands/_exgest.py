import commands2

from .intake import SetActive as SetIntakeActive
from .intake import SetInactive as SetIntakeInactive
from .feeder import SetActive as SetFeederActive
from .feeder import SetInactive as SetFeederInactive

import constants
import subsystems


class Exgest(commands2.CommandGroupBase):

    def __init__(self) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(subs)
        self._m_requirements
        self._intake_exgest = SetIntakeActive(constants.Intake.DEFAULT_EXGEST_SPEED).initialize
        self._intake_deactivate = SetIntakeInactive().initialize
        self._feeder_exgest = SetFeederActive(
            -constants.Feeder.TopMotors.DEFAULT_EXGEST_SPEED,
            -constants.Feeder.BottomMotors.DEFAULT_EXGEST_SPEED
        ).initialize
        self._feeder_deactivate = SetFeederInactive().initialize

    def initialize(self) -> None:
        self._intake_exgest()
        self._feeder_exgest()
        return super().initialize()

    def end(self, interrupted: bool) -> None:
        self._intake_deactivate()
        self._feeder_deactivate()
        return super().end(interrupted)
