import math
import commands2
from networktables import NetworkTables
import wpilib
import wpimath.geometry

import constants


class Limelight(commands2.SubsystemBase):
    """
    This subsystem is not intended to be required by any command.
    """
    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumberArray("Limelight/XYAV", [self.tx, self.ty, self.ta, self.tv])
        wpilib.SmartDashboard.putNumberArray("Limelight/nd", self._nd())
        wpilib.SmartDashboard.putNumberArray("Limelight/d", self._d())
        wpilib.SmartDashboard.putNumberArray("Limelight/components", self.component_distances)
        wpilib.SmartDashboard.putNumberArray("Limelight/distance", (self.distance, self.distance2))
        try:
            from subsystems import drivetrain
            from subsystems.shooter import turret
        except ImportError:
            pass
        else:
            drivetrain_pose = drivetrain.get_pose()
            turret_rotation = turret.get_robot_relative_rotation()
            # limelight_pose = drivetrain_pose.transformBy(
            #     wpimath.geometry.Transform2d(
            #         constants.Shooter.Turret.CENTER.rotateBy(drivetrain_pose.rotation())
            #       + constants.Limelight.TURRET_MOUNT_POSITION.rotateBy(drivetrain_pose.rotation() + turret_rotation),
            #         wpimath.geometry.Rotation2d(0)
            #     )
            # )
            limelight_pose = drivetrain_pose.transformBy(wpimath.geometry.Transform2d(wpimath.geometry.Translation2d(), turret_rotation))
            wpilib.SmartDashboard.putString("Limelight/Estimated Target Position", str(self.get_estimated_target_position(limelight_pose)))

        try:
            self.field.getObject('Limelight Hub Estimate').setPose(wpimath.geometry.Pose2d(self.get_estimated_target_position(drivetrain_pose), wpimath.geometry.Rotation2d()))
        except (NameError, AttributeError):
            self.field: wpilib.Field2d = wpilib.SmartDashboard.getData('Field')

    def __init__(self):
        commands2.SubsystemBase.__init__(self)
        self.setName('Limelight')

        self._table = NetworkTables.getTable('limelight')
        self._pipeline_entry = self._table.getEntry('pipeline')
        self._ledmode_entry = self._table.getEntry('ledMode')

        self._pipeline_entry.setDouble(constants.Limelight.PIPELINE)
        self._ledmode_entry.setDouble(0)

        self._MOUNT_ANGLE = constants.Limelight.MOUNT_ANGLE
        self._ACTUAL_HEIGHT = constants.Limelight.TARGET_HEIGHT - constants.Limelight.MOUNT_HEIGHT

    @property
    def tx(self):
        """The horizontal offset from crosshair to target."""
        return self._table.getNumber('tx', 0)

    @property
    def ty(self):
        """The vertical offset from crosshair to target."""
        return self._table.getNumber('ty', 0)

    @property
    def ta(self):
        """The relative size (distance) of the target."""
        return self._table.getNumber('ta', 0)

    @property
    def tv(self):
        """The number of targets being tracked (0 or 1)."""
        return self._table.getNumber('tv', 0)

    @property
    def y(self):
        """
        The normalized vertical distance to the target.

        Innacurate unless tx is 0
        """
        return math.sin(math.radians(self.ty + self._MOUNT_ANGLE))

    @property
    def z(self):
        """
        The normalized forward distance to the target.

        Innacurate unless tx is 0
        """
        return math.cos(math.radians(self.ty + self._MOUNT_ANGLE))

    def _nd(self):
        x = math.tan(math.radians(self.tx))
        y = math.tan(math.radians(self.ty))
        z = 1
        magnitude = math.sqrt(x**2 + y**2 + z**2)
        x, y, z = x/magnitude, y/magnitude, z/magnitude
        cos = math.cos(math.radians(-self._MOUNT_ANGLE))
        sin = math.sin(math.radians(-self._MOUNT_ANGLE))
        x, y, z = x, y * cos - z * sin, y * sin + z * cos # https://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
        return x, y, z

    def _d(self):
        x, y, z = self._nd()
        try:
            conversion_factor = self._ACTUAL_HEIGHT / y
        except ZeroDivisionError:
            return float('inf'), 0, float('inf')
        return x * conversion_factor, y * conversion_factor, z * conversion_factor

    @property
    def distance(self):
        return self._ACTUAL_HEIGHT / math.tan(math.radians(self.ty + self._MOUNT_ANGLE))

    @property
    def component_distances(self):
        return self.distance * math.sin(math.radians(self.tx)), self._ACTUAL_HEIGHT, self.distance * math.cos(math.radians(self.tx))

    @property
    def distance2(self):
        x, y, z = self._d()
        return (x ** 2 + z ** 2) ** 0.5

    def get_estimated_target_position(self, limelight_pose: wpimath.geometry.Pose2d):
        return limelight_pose.translation() + wpimath.geometry.Translation2d(self.distance + constants.Limelight.TARGET_RADIUS, limelight_pose.rotation() + wpimath.geometry.Rotation2d.fromDegrees(self.tx))

    @property
    def is_aligned(self):
        return self.tv == 1 and (math.fabs(self.tx) < constants.Limelight.X_TOLERANCE)

    @property
    def led_mode(self):
        self._ledmode_entry.getDouble(0)

    @led_mode.setter
    def led_mode(self, mode: int):
        self._ledmode_entry.setDouble(mode)
