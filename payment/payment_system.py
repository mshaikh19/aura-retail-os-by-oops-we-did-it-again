from payment.adapters.upi_adapter import UPIAdapter


class PaymentSystem:

    def makePayment(self, method, amount):
        print("\n[PaymentSystem] Starting payment...")

        if method == "UPI":
            processor = UPIAdapter()
        else:
            print("[PaymentSystem] Invalid payment method")
            return

        processor.processPayment(amount)

        print("[PaymentSystem] Payment completed")

    def refund(self, method, amount):
        print("\n[PaymentSystem] Starting refund...")

        if method == "UPI":
            processor = UPIAdapter()
        else:
            print("[PaymentSystem] Invalid payment method")
            return

        processor.refundPayment(amount)

        print("[PaymentSystem] Refund completed")