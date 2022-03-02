# (lambda w,d,c:(lambda r,i:(setattr(r,'teleopInit',lambda s: setattr(s,'d',w.drive.DifferentialDrive(c.WPI_TalonFX(0),c.WPI_TalonFX(1)))),setattr(r,'teleopPeriodic',lambda s: s.d.arcadeDrive(i.getLeftX(),i.getRightY())),w.run(r)))(type('r',(w.TimedRobot,),{}),w.XboxController(0)))(*(lambda i:(i('wpilib'),i('wpilib.drive'),i('ctre')))(__import__))

# import wpilib as w
# import wpilib.drive as d
# from ctre import WPI_TalonFX as t
# class r(w.TimedRobot):
#  def teleopInit(s):
#   s.d=d.DifferentialDrive(t(0),t(1))
#   s.c=w.XboxController(0)
#  def teleopPeriodic(s):
#   s.d.arcadeDrive(s.c.getLeftX(),s.c.getRightY())

import wpilib
import ctre
class Robot(wpilib.TimedRobot):
    def teleopInit(self) -> None:
        self.ms = (ctre.WPI_TalonFX(i) for i in (2, 6, 7, 8))
        for m in self.ms:
            m.setNeutralMode(ctre.NeutralMode.Coast)
        return super().teleopInit()
