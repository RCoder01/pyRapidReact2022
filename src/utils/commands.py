import commands2


class RepeatCommand(commands2.CommandBase):
    def __init__(self, command: commands2.Command) -> None:
        commands2.CommandBase.__init__(self)

        self.addRequirements(command.getRequirements())
        self.setName(command.getName())

        self._command = command

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


def set_name(command: commands2.Command, name: str):
    if isinstance(command, commands2.CommandBase):
        command.setName(name)
    else:
        command.getName = lambda self: name
    return command
