from abc import ABC, abstractmethod

# This is a base class for all payment methods
class PaymentProcessor(ABC):

    # Every payment method must implement these functions
    @abstractmethod
    def processPayment(self, amount):
        pass

    @abstractmethod
    def refundPayment(self, amount):
        pass