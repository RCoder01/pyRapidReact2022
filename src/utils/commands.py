import commands2


class RepeatCommand(commands2.CommandBase):
    def __init__(self, command: commands2.Command = None) -> None:
        commands2.CommandBase.__init__(self)
        if command:
            self.addRequirements(command.getRequirements())
            self.setName(command.getName())

        self._command = command or self

    def initialize(self) -> None:
        return self._command.initialize()

    def execute(self) -> None:
        retval = self._command.execute()

        if self._command.isFinished():
            self._command.end(False)
            self._command.initialize()

        return retval

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        return self._command.end(interrupted)
