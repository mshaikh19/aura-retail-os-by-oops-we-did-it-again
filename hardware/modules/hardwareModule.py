from abc import ABC, abstractmethod

class HardwareModule(ABC):
    """
    DECORATOR PATTERN - Abstract Component
    Base class for optional hardware add-ons.
    """
    
    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def deactivate(self):
        pass

    @abstractmethod
    def getStatus(self) -> dict:
        """ Returns a status dictionary of the module and any wrapped modules """
        pass
