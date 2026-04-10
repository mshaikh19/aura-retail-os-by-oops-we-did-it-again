from .command import Command


class RestockCommand(Command):
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def execute(self, core):
        name = self.product.model.name if hasattr(self.product, "model") else getattr(self.product, "name", str(self.product))
        print(f"[Restock] Adding {self.quantity} units of {name}")

        if hasattr(self.product, "addStock"):
            self.product.addStock(self.quantity)
        elif core.inventorySystem:
            print("[Restock] Updating inventory...")

        print("[Restock] Restock completed successfully.")

        self.log()