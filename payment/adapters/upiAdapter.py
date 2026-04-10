from payment.interfaces.paymentProcessor import PaymentProcessor

#UPIAdapter handles UPI-specific payment logic. It follows the structure defined by PaymentProcessor
class UPIAdapter(PaymentProcessor):

    def processPayment(self, amount):
        print(f"[UPI] Processing ₹{amount}")
        return True

    def refundPayment(self, amount):
        print(f"[UPI] Refunding ₹{amount}")
        return True