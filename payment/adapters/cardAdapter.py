from payment.interfaces.paymentProcessor import PaymentProcessor

# CardAdapter handles Card-specific payment logic (Adapter Pattern)
class CardAdapter(PaymentProcessor):

    def processPayment(self, amount):
        print(f"[CARD] Processing ₹{amount}")

        # collect card details
        card_number = input("Enter Card Number (16 digits): ")
        cvv = input("Enter CVV (3 digits): ")
        expiry = input("Enter Expiry (MM/YY): ")

        # basic validation
        if len(card_number) != 16 or not card_number.isdigit():
            print("[CARD] Invalid card number")
            return False, {}

        if len(cvv) != 3 or not cvv.isdigit():
            print("[CARD] Invalid CVV")
            return False, {}

        if len(expiry) != 5 or expiry[2] != '/':
            print("[CARD] Invalid expiry format")
            return False, {}

        confirm = input("Confirm payment? (y/n): ").lower()
        if confirm != "y":
            print("[CARD] Payment cancelled")
            return False, {}

        print(f"[CARD] Payment of ₹{amount} successful")

        # return minimal safe details
        return True, {"card_last4": card_number[-4:]}

    def refundPayment(self, amount):
        print(f"[CARD] Refunding ₹{amount}")
        return True