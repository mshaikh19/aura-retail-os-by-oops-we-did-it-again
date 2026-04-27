from abc import ABC, abstractmethod


class DispenserInterface(ABC):
    """
    Bridge Pattern — Implementation Interface

    This defines the contract for all dispenser types.
    """

    @abstractmethod
    def dispense(self, product_name: str, quantity: int) -> bool:
        """
        Dispense given quantity of product.
        Returns True if successful.
        """
        pass

    @abstractmethod
    def calibrate(self) -> bool:
        """
        Perform calibration of hardware.
        Returns True if successful.
        """
        pass

    @abstractmethod
    def getStatus(self) -> str:
        """
        Returns current status of dispenser.
        """
        pass

    @abstractmethod
    def isSlotJammed(self, product_name: str) -> bool:
        """
        Returns True if the specific slot for a product is jammed.
        """
        pass