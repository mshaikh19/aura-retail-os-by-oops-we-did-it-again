from abc import ABC, abstractmethod

class PaymentProcessor(ABC):

    @abstractmethod
    def processPayment(self, amount):
        pass

    @abstractmethod
    def refundPayment(self, amount):
        pass