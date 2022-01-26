import typing

from wpilib import XboxController
from wpilib.interfaces import GenericHID

from ._template import BaseInput

class XboxDriverController(BaseInput):
    def __init__(self):
        super().__init__()
        self.mController = XboxController(0)

    @typing.override
    def get_left_speed(self) -> float:
        return self.mController.getY(GenericHID.Hand.kLeftHand)

    @typing.override
    def get_right_speed(self) -> float:
        return self.mController.getY(GenericHID.Hand.kRightHand)