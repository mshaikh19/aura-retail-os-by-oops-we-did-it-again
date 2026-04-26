from .command import Command
from utils.colors import Colors
import random


class PurchaseCommand(Command):

    def __init__(self, product, quantity, paymentMethod):
        self.product = product
        self.quantity = quantity
        self.paymentMethod = paymentMethod
        self.last_transaction = None

    def execute(self, core):

        print(f"{Colors.HEADER}[Purchase]{Colors.RESET} Attempting to purchase {self.quantity} of {self.product.getName()}")

        # ---------------- VALIDATION ---------------- #

        if self.product is None:
            raise Exception("Invalid product")

        if self.product.getAvailableStock() < self.quantity:
            raise Exception("Not enough stock")

        # ---------------- TASK 7.2: HARDWARE DEPENDENCY ---------------- #

        required_module = getattr(self.product.model, "required_module", None)

        if required_module:
            active_modules = core.getActiveModuleNames()

            if required_module not in active_modules:
                raise Exception(f"{self.product.getName()} requires {required_module.upper()} module")

        # ---------------- PRICE ---------------- #

        totalAmount = self.product.getPrice() * self.quantity
        print(f"{Colors.HEADER}[Purchase]{Colors.RESET} Total amount: ₹{totalAmount}")

        if core.paymentSystem is None:
            raise Exception("Payment system unavailable")

        # ---------------- PAYMENT ---------------- #

        transaction = core.paymentSystem.makePayment(
            self.paymentMethod,
            totalAmount,
            self.product.getName(),
            self.quantity,
            kiosk_type=core.kioskType
        )

        if not transaction:
            raise Exception("Payment failed")

        self.last_transaction = transaction

        # ---------------- HARDWARE DISPENSE ---------------- #

        if core.hardwareSystem:
            print(f"{Colors.HEADER}[Purchase]{Colors.RESET} Sending request to hardware...")

            success = core.hardwareSystem.dispenseProduct(
                self.product.getName(),
                self.quantity
            )

            # ---------------- TASK 7.3: FAILURE SIMULATION ---------------- #
            if random.random() < 0.2:   # 20% failure chance
                print(f"{Colors.ERROR}[HARDWARE]{Colors.RESET} Simulated hardware failure")
                success = False

            # ---------------- ATOMIC TRANSACTION (4.2) ---------------- #
            if not success:
                print(f"{Colors.ERROR}[Purchase]{Colors.RESET} Dispense failed — rolling back")

                # rollback payment
                core.paymentSystem.refund(self.paymentMethod)

                # system goes into error state
                core.setSystemStatus("ERROR")

                raise Exception("Transaction rolled back due to hardware failure")

        # ---------------- INVENTORY UPDATE ---------------- #

        if core.inventorySystem:
            product_key = core.inventorySystem.findKeyForProduct(self.product)

            if product_key:
                core.inventorySystem.reduceStock(product_key, self.quantity)
            else:
                self.product.reduceStock(self.quantity)
        else:
            self.product.reduceStock(self.quantity)

        print(f"{Colors.HEADER}[Purchase]{Colors.RESET} Purchase completed successfully.")

        self.log()
        return True