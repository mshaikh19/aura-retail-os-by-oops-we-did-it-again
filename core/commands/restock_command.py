from .command import Command


class RestockCommand(Command):
    def __init__(self, productName, quantity):
        self.productName = productName
        self.quantity = quantity

    def execute(self, core):
        print(f"[Restock] Adding {self.quantity} units of {self.productName}")

        if core.inventorySystem:
            print("[Restock] Updating inventory...")

        print("[Restock] Restock completed successfully.")

        self.log()