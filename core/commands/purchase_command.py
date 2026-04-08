from .command import Command


class PurchaseCommand(Command):
    def __init__(self, product, quantity, paymentMethod):
        self.product = product
        self.quantity = quantity
        self.paymentMethod = paymentMethod

    def execute(self, core):
        print(f"[Purchase] Attempting to purchase {self.quantity} of {self.product.model.name}")

        # 1. Validate product
        if self.product is None:
            raise Exception("Invalid product")

        # 2. Check stock
        if self.product.getStock() < self.quantity:
            raise Exception("Not enough stock")

        # 3. Calculate total price
        totalAmount = self.product.getPrice() * self.quantity
        print(f"[Purchase] Total amount: ₹{totalAmount}")

        # 4. Process payment
        if core.paymentSystem is None:
            raise Exception("Payment system unavailable")

        core.paymentSystem.makePayment(self.paymentMethod, totalAmount)

        # 5. Reduce stock (only after payment)
        self.product.reduceStock(self.quantity)

        print("[Purchase] Purchase completed successfully.")
        self.log()