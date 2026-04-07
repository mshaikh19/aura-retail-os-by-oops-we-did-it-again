from payment.interfaces.payment_processor import PaymentProcessor

class UPIAdapter(PaymentProcessor):

    def processPayment(self, amount):
        print(f"[UPI] Processing ₹{amount}")
        return True

    def refundPayment(self, amount):
        print(f"[UPI] Refunding ₹{amount}")
        return True