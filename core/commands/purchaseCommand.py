from .command import Command


class PurchaseCommand(Command):
    # concrete command for handling purchase operation

    def __init__(self, product, quantity, paymentMethod):
        self.product = product
        self.quantity = quantity
        self.paymentMethod = paymentMethod

    def execute(self, core):
        print(f"[Purchase] Attempting to purchase {self.quantity} of {self.product.model.name}")

        # validate product
        if self.product is None:
            raise Exception("Invalid product")

        # check stock availability
        if self.product.getStock() < self.quantity:
            raise Exception("Not enough stock")

        # calculate total price
        totalAmount = self.product.getPrice() * self.quantity
        print(f"[Purchase] Total amount: ₹{totalAmount}")

        # ensure payment system exists
        if core.paymentSystem is None:
            raise Exception("Payment system unavailable")

        # process payment
        paymentSuccess = core.paymentSystem.makePayment(self.paymentMethod, totalAmount)

        if not paymentSuccess:
            raise Exception("Payment failed")

        # 🔥 hardware integration (Bridge Pattern)
        if core.hardwareSystem:
            print("[Purchase] Sending request to hardware...")

            success = core.hardwareSystem.dispenseProduct(
                self.product.model.name,   # ✅ correct access
                self.quantity
            )

            if not success:
                raise Exception("Dispense failed — transaction cancelled")

        # update inventory ONLY after successful payment + dispense
        self.product.reduceStock(self.quantity)

        print("[Purchase] Purchase completed successfully.")

        self.log()  # common logging