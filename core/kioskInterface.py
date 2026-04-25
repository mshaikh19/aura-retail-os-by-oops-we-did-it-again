from core.commands.purchaseCommand import PurchaseCommand
from core.commands.refundCommand import RefundCommand
from core.commands.restockCommand import RestockCommand


class KioskInterface:
    """
        FACADE PATTERN
        Single entry point for all external interactions.
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
        
        # Display operational status of the kiosk
        operational_status = getattr(self.core, 'getOperationalStatus', lambda: self.core.getSystemStatus())()
        print(f"Operational Status: {operational_status}")
        
        # Display hardware modules status of the kiosk if any
        if hasattr(self.core, 'getModuleStatuses'):
            modules_status = self.core.getModuleStatuses()
            if modules_status:
                print("Attached Modules Status:")
                for module_name, status in modules_status.items():
                    print(f"  - {module_name}: {status}")
        
        # Fetch alerts from Monitoring System
        try:
            from monitoring.monitoring_system import MonitoringSystem
            MonitoringSystem.showAlerts()
        except ImportError:
            pass