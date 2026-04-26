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
        import time
        print(f"\n{Colors.CYAN}[INTERFACE]{Colors.RESET} Processing {Colors.BOLD}{quantity}{Colors.RESET} unit request...")
        time.sleep(0.4)

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
            print(f"{Colors.ERROR}Invalid input for refund{Colors.RESET}")
            return
        
        import time
        print(f"\n{Colors.CYAN}[INTERFACE]{Colors.RESET} Refund request: {Colors.BOLD}Rs.{amount}{Colors.RESET}")
        time.sleep(0.4)

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
            print(f"{Colors.ERROR}Invalid input for restock{Colors.RESET}")
            return
        
        import time
        print(f"\n{Colors.CYAN}[INTERFACE]{Colors.RESET} Restock request: {Colors.BOLD}{quantity}{Colors.RESET} units")
        time.sleep(0.4)

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
        
        print("\n" + Colors.BLUE + " ╔" + "═"*58 + "╗" + Colors.RESET)
        print(f" {Colors.BLUE}║{Colors.RESET}           {Colors.BOLD}{Colors.CYAN}❖ SYSTEM DIAGNOSTICS ENGINE{Colors.RESET}            {Colors.BLUE}║{Colors.RESET}")
        print(Colors.BLUE + " ╠" + "═"*58 + "╣" + Colors.RESET)
        
        # 1. Render Core Section
        core_data = data["CORE"]
        status_color = Colors.SUCCESS if core_data["AuraCore Integrity"] == "ACTIVE" else Colors.ERROR
        print(f" {Colors.BLUE}║{Colors.RESET}  {Colors.BOLD}AURACORE INTEGRITY:{Colors.RESET}".ljust(66) + f"{Colors.BLUE}║{Colors.RESET}")
        print(f" {Colors.BLUE}║{Colors.RESET}   > Status:      {status_color}{core_data['AuraCore Integrity']}{Colors.RESET}".ljust(75) + f"{Colors.BLUE}║{Colors.RESET}")
        print(f" {Colors.BLUE}║{Colors.RESET}   > Personality: {Colors.TEXT}{core_data['Kiosk Personality']}{Colors.RESET}".ljust(75) + f"{Colors.BLUE}║{Colors.RESET}")
        print(f" {Colors.BLUE}║{Colors.RESET}   > Activity:    {Colors.DIM}{core_data['Activity Ledger']}{Colors.RESET}".ljust(75) + f"{Colors.BLUE}║{Colors.RESET}")
        
        print(Colors.BLUE + " ╟" + "─"*58 + "╢" + Colors.RESET)
        
        # 2. Render Hardware Section
        hw = data["HARDWARE"]
        print(f" {Colors.BLUE}║{Colors.RESET}  {Colors.BOLD}HARDWARE STACK:{Colors.RESET}".ljust(66) + f"{Colors.BLUE}║{Colors.RESET}")
        print(f" {Colors.BLUE}║{Colors.RESET}   > Dispense Node: {Colors.HEADER}{hw['Dispensing Node']}{Colors.RESET}".ljust(75) + f"{Colors.BLUE}║{Colors.RESET}")
        print(f" {Colors.BLUE}║{Colors.RESET}   > Kinetic Drive: {Colors.DIM}{hw['Kiosk Motor Module']}{Colors.RESET}".ljust(75) + f"{Colors.BLUE}║{Colors.RESET}")
        
        # 3. Render Extensions Section (if any)
        ext = data["EXTENSIONS"]
        if ext:
            print(Colors.BLUE + " ╟" + "─"*58 + "╢" + Colors.RESET)
            print(f" {Colors.BLUE}║{Colors.RESET}  {Colors.BOLD}ACTIVE EXTENSIONS:{Colors.RESET}".ljust(66) + f"{Colors.BLUE}║{Colors.RESET}")
            for key, val in ext.items():
                print(f" {Colors.BLUE}║{Colors.RESET}   + {key.upper():<12} {Colors.SUCCESS}{val}{Colors.RESET}".ljust(75) + f"{Colors.BLUE}║{Colors.RESET}")
        
        print(Colors.BLUE + " ╚" + "═"*58 + "╝" + Colors.RESET)
        return True
        
        # Fetch alerts from Monitoring System
        try:
            from monitoring.monitoring_system import MonitoringSystem
            MonitoringSystem.showAlerts()
        except ImportError:
            pass