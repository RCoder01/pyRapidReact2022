import commands2

import subsystems

from ._elevate_ball import ElevateBall
from ._monitor import Monitor
from ._set_active import SetActive
from ._set_inactive import SetInactive

# ElevateBall = commands2.ParallelCommandGroup(
#     SetActive,
#     commands2.WaitUntilCommand(subsystems.feeder.get_out_sensor),
#     SetInactive
# )
