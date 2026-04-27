from abc import ABC, abstractmethod

class PricingPolicy(ABC):
    """
    Strategy Pattern - Strategy Interface
    Defines how product prices should be calculated.
    """
    @abstractmethod
    def calculatePrice(self, base_price: float) -> float:
        pass

class StandardPricingPolicy(PricingPolicy):
    """
    Returns the standard price without any modifications.
    """
    def calculatePrice(self, base_price: float) -> float:
        return base_price

class DiscountedPricingPolicy(PricingPolicy):
    """
    Applies a discount to the base price.
    """
    def __init__(self, discount_percent=0.1):
        self.discount_percent = discount_percent

    def calculatePrice(self, base_price: float) -> float:
        return base_price * (1.0 - self.discount_percent)

class EmergencyPricingPolicy(PricingPolicy):
    """
    Applies a markup to the base price for emergency situations.
    """
    def __init__(self, markup_percent=0.2):
        self.markup_percent = markup_percent

    def calculatePrice(self, base_price: float) -> float:
        return base_price * (1.0 + self.markup_percent)
