import commands2

import subsystems

from ._set_active import SetActive
from ._set_inactive import SetInactive


class ElevateBall(commands2.SequentialCommandGroup):
    def __init__(self) -> None:
        commands2.SequentialCommandGroup.__init__(
            self,
            SetActive(),
            commands2.WaitUntilCommand(subsystems.feeder.get_out_sensor),
            SetInactive(),
        )
        self.setName("Elevate Ball")
