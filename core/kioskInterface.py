from core.commands.purchase_command import PurchaseCommand
from core.commands.refund_command import RefundCommand
from core.commands.restock_command import RestockCommand


class KioskInterface:
    def __init__(self, coreSystem):
        self.core = coreSystem

    def purchaseItem(self, productId, quantity):
        if not productId or quantity <= 0:
            print("Invalid input for purchase")
            return
        
        print(f"[INTERFACE] Purchase request: {quantity} x {productId}")

        command = PurchaseCommand(productId, quantity)
        self.core.executeCommand(command)

    def refundTransaction(self, productId, quantity):
        if not productId or quantity <= 0:
            print("Invalid input for refund")
            return
        
        print(f"[INTERFACE] Refund request: {quantity} x {productId}")

        command = RefundCommand(productId, quantity)
        self.core.executeCommand(command)

    def restockInventory(self, productId, quantity):
        if not productId or quantity <= 0:
            print("Invalid input for restock")
            return
        
        print(f"[INTERFACE] Restock request: {quantity} x {productId}")

        command = RestockCommand(productId, quantity)
        self.core.executeCommand(command)

    def runDiagnostics(self):
        print("[INTERFACE] Running diagnostics...")
        print(f"System Status: {self.core.getSystemStatus()}")