class Command:
    def execute(self, core):
        raise NotImplementedError("Execute method must be implemented")

    def undo(self, core):
        pass

    def log(self):
        print(f"[COMMAND] {self.__class__.__name__} executed")