from core.commands.purchaseCommand import PurchaseCommand
from core.commands.refundCommand import RefundCommand
from core.commands.restockCommand import RestockCommand
from utils.colors import Colors


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
    def refundTransaction(self, paymentMethod):
        """
            Safety Check :
                If amount is less than or equal to 0, return
        """
        
        print("[INTERFACE] Refund request for last transaction")

        """
            Create a command object to pass to the core system for refunding transaction
        """

        command = RefundCommand(paymentMethod)
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
        """
        FACADE PATTERN
        Unified interface for checking all subsystem health.
        """
        data = self.core.getOperationalStatus()
        
        # Prepare lines for drawBox
        core_info = data["CORE"]
        hw_info = data["HARDWARE"]
        ext_info = data["EXTENSIONS"]
        
        status_color = Colors.SUCCESS if core_info["System Status"] == "ACTIVE" else Colors.ERROR
        
        lines = [
            f"{Colors.BOLD}CORE STATUS:{Colors.RESET}",
            f" > Status:      {status_color}{core_info['System Status']}{Colors.RESET}",
            f" > Application: {Colors.TEXT}{core_info['Kiosk Type']}{Colors.RESET}",
            f" > History:     {Colors.DIM}{core_info['Command Logs']}{Colors.RESET}",
            "",
            f"{Colors.BOLD}HARDWARE ENGINE:{Colors.RESET}",
            f" > Dispenser:   {Colors.HEADER}{hw_info['Dispenser']}{Colors.RESET}",
            f" > Motor Unit:  {Colors.DIM}{hw_info['Motor Module']}{Colors.RESET}"
        ]
        
        if ext_info:
            lines.append("")
            lines.append(f"{Colors.BOLD}ACTIVE EXTENSIONS:{Colors.RESET}")
            for key, val in ext_info.items():
                lines.append(f" + {key.upper():<12} {Colors.SUCCESS}{val}{Colors.RESET}")
        
        from main import drawBox # Import helper
        drawBox("❖ SYSTEM DIAGNOSTICS ENGINE", lines, color=Colors.CYAN)
        
        return True
        
        # Fetch alerts from Monitoring System
        try:
            from monitoring.monitoring_system import MonitoringSystem
            MonitoringSystem.showAlerts()
        except ImportError:
            pass