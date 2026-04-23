# Import adapter classes for different payment methods
from payment.adapters.upiAdapter import UPIAdapter
from payment.adapters.cardAdapter import CardAdapter
from payment.adapters.walletAdapter import WalletAdapter


class PaymentSystem:

    def makePayment(self, method, amount):
        print("\n[PaymentSystem] Starting payment...")

        # Dynamically get the correct payment processor (Adapter)
        processor = self._getProcessor(method)
        if processor is None:
            print("[PaymentSystem] Invalid payment method")
            return False

        # Calls the same method, but different adapters handle it in their own way
        result = processor.processPayment(amount)

        print("[PaymentSystem] Payment completed")
        return result

    def refund(self, method, amount):
        print("\n[PaymentSystem] Starting refund...")

        processor = self._getProcessor(method)
        if processor is None:
            print("[PaymentSystem] Invalid payment method")
            return False

        result = processor.refundPayment(amount)

        print("[PaymentSystem] Refund completed")
        return result

    #Method to select and return the appropriate payment adapter.
    def _getProcessor(self, method):
        if method == "UPI":
            return UPIAdapter()
        elif method == "CARD":
            return CardAdapter()
        elif method == "WALLET":
            return WalletAdapter()
        else:
            return None