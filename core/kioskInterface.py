from core.commands.purchase_command import PurchaseCommand
from core.commands.refund_command import RefundCommand
from core.commands.restock_command import RestockCommand


class KioskInterface:
    def __init__(self, coreSystem):
        self.core = coreSystem

    def purchaseItem(self, product, quantity, paymentMethod):
        if not product or quantity <= 0:
            print("Invalid input for purchase")
            return
        
        print(f"[INTERFACE] Purchase request: {quantity} units")

        command = PurchaseCommand(product, quantity, paymentMethod)
        self.core.executeCommand(command)

    def refundTransaction(self, amount, paymentMethod):
        if amount <= 0:
            print("Invalid input for refund")
            return
        
        print(f"[INTERFACE] Refund request: \u20b9{amount}")

        command = RefundCommand(amount, paymentMethod)
        self.core.executeCommand(command)

    def restockInventory(self, product, quantity):
        if not product or quantity <= 0:
            print("Invalid input for restock")
            return
        
        print(f"[INTERFACE] Restock request: {quantity} units")

        command = RestockCommand(product, quantity)
        self.core.executeCommand(command)

    def runDiagnostics(self):
        print("[INTERFACE] Running diagnostics...")
        print(f"System Status: {self.core.getSystemStatus()}")