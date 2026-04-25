from abc import ABC, abstractmethod

class InventoryComponent(ABC):
    """
    Composite Pattern - Component Interface
    Shared interface for both individual products and product bundles.
    """

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def getPrice(self) -> float:
        pass

    @abstractmethod
    def getAvailableStock(self) -> int:
        pass

    @abstractmethod
    def reduceStock(self, qty: int):
        pass

    @abstractmethod
    def isAvailable(self) -> bool:
        pass

    @abstractmethod
    def display(self, indent=0):
        pass
