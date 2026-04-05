from .command import Command


class PurchaseCommand(Command):
    def __init__(self, productName, quantity):
        self.productName = productName
        self.quantity = quantity

    def execute(self, core):
        print(f"[Purchase] Attempting to purchase {self.quantity} of {self.productName}")

        # Dummy logic for now
        if core.inventorySystem:
            print("[Purchase] Checking inventory...")

        if core.paymentSystem:
            print("[Purchase] Processing payment...")

        if core.hardwareSystem:
            print("[Purchase] Dispensing product...")

        print("[Purchase] Purchase completed successfully.")

        self.log()