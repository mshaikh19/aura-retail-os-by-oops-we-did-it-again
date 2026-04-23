from payment.interfaces.paymentProcessor import PaymentProcessor

#CardAdapter handles Card-specific payment logic. It follows the structure defined by PaymentProcessor
class CardAdapter(PaymentProcessor):

    def processPayment(self, amount):
        print(f"[CARD] Processing ₹{amount}")
        return True

    def refundPayment(self, amount):
        print(f"[CARD] Refunding ₹{amount}")
        return True