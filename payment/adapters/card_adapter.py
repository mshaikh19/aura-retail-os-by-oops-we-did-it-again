from payment.interfaces.payment_processor import PaymentProcessor

class CardAdapter(PaymentProcessor):

    def processPayment(self, amount):
        print(f"[CARD] Processing ₹{amount}")
        return True

    def refundPayment(self, amount):
        print(f"[CARD] Refunding ₹{amount}")
        return True