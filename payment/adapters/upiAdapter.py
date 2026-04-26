from payment.interfaces.paymentProcessor import PaymentProcessor

# UPIAdapter handles UPI-specific payment logic (Adapter Pattern)
class UPIAdapter(PaymentProcessor):

    def processPayment(self, amount):
        print(f"[UPI] Processing ₹{amount}")

        # collect UPI details
        upi_id = input("Enter UPI ID (e.g., user@upi): ")

        # basic validation
        if "@" not in upi_id or len(upi_id.split("@")) != 2:
            print("[UPI] Invalid UPI ID")
            return False, {}

        confirm = input("Confirm payment? (y/n): ").lower()
        if confirm != "y":
            print("[UPI] Payment cancelled")
            return False, {}

        print(f"[UPI] Payment of ₹{amount} successful via {upi_id}")

        # return minimal details
        return True, {"upi_id": upi_id}

    def refundPayment(self, amount):
        print(f"[UPI] Refunding ₹{amount}")
        return True