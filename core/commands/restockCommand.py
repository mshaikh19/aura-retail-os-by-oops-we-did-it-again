from .command import Command


class RestockCommand(Command):
    # concrete command for updating inventory (Command Pattern)

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def execute(self, core):
        # validate product
        if self.product is None:
            raise Exception("Invalid product")

        # validate quantity
        if self.quantity <= 0:
            raise Exception("Invalid quantity")

        print(f"[Restock] Adding {self.quantity} units of {self.product.getName()}")
        
        # update stock using core inventory system (to trigger Proxy/Persistence)
        if core.inventorySystem:
            product_key = core.inventorySystem.findKeyForProduct(self.product)
            if product_key:
                core.inventorySystem.addStock(product_key, self.quantity)
                print(f"[Restock] New stock in system: {self.product.getAvailableStock()}")
            else:
                self.product.addStock(self.quantity)
        else:
            # fallback to direct update
            self.product.addStock(self.quantity)

        print("[Restock] Restock completed successfully.")

        self.log()  # log execution