from payment.interfaces.payment_processor import PaymentProcessor

class WalletAdapter(PaymentProcessor):

    def processPayment(self, amount):
        print(f"[WALLET] Processing ₹{amount}")
        return True

    def refundPayment(self, amount):
        print(f"[WALLET] Refunding ₹{amount}")
        return True