from payment.interfaces.paymentProcessor import PaymentProcessor

#WalletAdapter handles Wallet-specific payment logic. It follows the structure defined by PaymentProcessor
class WalletAdapter(PaymentProcessor):

    def processPayment(self, amount):
        print(f"[WALLET] Processing ₹{amount}")
        return True, {}

    def refundPayment(self, amount):
        print(f"[WALLET] Refunding ₹{amount}")
        return True