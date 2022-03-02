import typing
import warnings

import utils.warnings

from ._to_hub_angle import ToHubAngle


class ToVariableHubAngle(ToHubAngle):
    class HubAngleOverrideWarning(utils.warnings.SetpointOverrideWarning): pass

    def __init__(self, hub_angle_supplier: typing.Callable[[], float]):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=self.HubAngleOverrideWarning)
            super().__init__(hub_angle_supplier())

        self.setName('Turret to Variable Hub Angle')

        self._hub_angle_supplier = hub_angle_supplier

    @property
    def _hub_angle(self):
        return self._hub_angle_supplier()

    @_hub_angle.setter
    def _hub_angle(self, value):
        warnings.warn("Hub angle setpoint is read-only", self.HubAngleOverrideWarning)
