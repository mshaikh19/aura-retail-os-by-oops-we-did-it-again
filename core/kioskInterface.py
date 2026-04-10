from core.commands.purchase_command import PurchaseCommand
from core.commands.refund_command import RefundCommand
from core.commands.restock_command import RestockCommand


class KioskInterface:
    """
        Initialize the interface
    """
    def __init__(self, coreSystem):
        self.core = coreSystem

    """
        Create a purchase item function to simulate the purchase of item 
    """
    def purchaseItem(self, product, quantity, paymentMethod):
        """
            Safety Check :
                If product is not found or quantity is less than or equal to 0, return
        """
        if not product or quantity <= 0:
            print("Invalid input for purchase")
            return

        """
            Process the request
        """
        print(f"[INTERFACE] Purchase request: {quantity} units")

        """
            Create a command object to pass to the core system for purchasing product
        """
        command = PurchaseCommand(product, quantity, paymentMethod)
        self.core.executeCommand(command)

    """
        Create a refund transaction function to simulate the refund of transaction 
    """
    def refundTransaction(self, amount, paymentMethod):
        """
            Safety Check :
                If amount is less than or equal to 0, return
        """
        if amount <= 0:
            print("Invalid input for refund")
            return
        
        print(f"[INTERFACE] Refund request: \u20b9{amount}")

        """
            Create a command object to pass to the core system for refunding transaction
        """

        command = RefundCommand(amount, paymentMethod)
        self.core.executeCommand(command)

    """
        Create a restock inventory function to simulate the restock of inventory 
    """
    def restockInventory(self, product, quantity):
        """
            Safety Check :
                If product is not found or quantity is less than or equal to 0, return
        """
        if not product or quantity <= 0:
            print("Invalid input for restock")
            return
        
        print(f"[INTERFACE] Restock request: {quantity} units")

        """
            Create a command object to pass to the core system for restocking inventory
        """
        command = RestockCommand(product, quantity)
        self.core.executeCommand(command)

    """
        Create a diagnostics function to simulate the diagnostics of the system 
    """
    
    def runDiagnostics(self):
        print("[INTERFACE] Running diagnostics...")
        print(f"System Status: {self.core.getSystemStatus()}")