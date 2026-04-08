from payment.adapters.upi_adapter import UPIAdapter
from payment.adapters.card_adapter import CardAdapter
from payment.adapters.wallet_adapter import WalletAdapter


class PaymentSystem:

    def makePayment(self, method, amount):
        print("\n[PaymentSystem] Starting payment...")

        processor = self._getProcessor(method)
        if processor is None:
            print("[PaymentSystem] Invalid payment method")
            return False

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

    def _getProcessor(self, method):
        if method == "UPI":
            return UPIAdapter()
        elif method == "CARD":
            return CardAdapter()
        elif method == "WALLET":
            return WalletAdapter()
        else:
            return None