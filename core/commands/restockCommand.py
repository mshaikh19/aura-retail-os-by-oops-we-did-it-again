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

        # update stock using product method (encapsulation)
        self.product.addStock(self.quantity)

        print(f"[Restock] New stock: {self.product.getStock()}")
        print("[Restock] Restock completed successfully.")

        self.log()  # log execution