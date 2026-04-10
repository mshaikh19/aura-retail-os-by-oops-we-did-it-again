class Command:
    # base class for all commands (Command Pattern)

    def execute(self, core):
        # must be implemented by child classes
        raise NotImplementedError("Execute method must be implemented")

    def undo(self, core):
        # optional for future use
        pass

    def log(self):
        # common logging for all commands
        print(f"[COMMAND] {self.__class__.__name__} executed")