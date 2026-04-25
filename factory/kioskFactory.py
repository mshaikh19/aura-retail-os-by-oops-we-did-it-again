from abc import ABC, abstractmethod

class KioskFactory(ABC):
    """
    ABSTRACT FACTORY PATTERN
    Interface for creating families of related hardware components.
    """
    
    @abstractmethod
    def createDispenser(self):
        """ Returns a concrete DispenserInterface implementation """
        pass

    @abstractmethod
    def getKioskType(self) -> str:
        """ Returns the readable name of the kiosk type """
        pass

    @abstractmethod
    def getDefaultInventory(self) -> dict:
        """ Returns application-specific starting data """
        pass
