from core.commands.purchaseCommand import PurchaseCommand
from core.commands.refundCommand import RefundCommand
from core.commands.restockCommand import RestockCommand
from utils.colors import Colors


from utils.ui_utils import pad_ansi

class KioskInterface:
    """
        FACADE PATTERN
        Single entry point for all external interactions.
        Initialize the interface
    """
    def __init__(self, coreSystem):
        from monitoring.monitoring_system import MonitoringSystem
        self.core = coreSystem
        MonitoringSystem.notify(source="INTERFACE", event_type="FACADE_READY", detail="Unified Interface Facade access point online.")

    """
        Create a purchase item function to simulate the purchase of item 
    """
    def purchaseItem(self, product, quantity, paymentMethod):
        """
            Safety Check :
                If product is not found or quantity is less than or equal to 0, return
        """
        if not product or quantity <= 0:
            print(f"{Colors.ERROR}[INTERFACE ERROR]{Colors.RESET} Invalid input for purchase")
            return

        """
            Process the request
        """
        print(f"{Colors.CYAN}[INTERFACE]{Colors.RESET} Purchase request: {quantity} units")

        """
            Create a command object to pass to the core system for purchasing product
        """
        command = PurchaseCommand(product, quantity, paymentMethod)
        self.core.executeCommand(command)

    def isRefundAvailable(self):
        """
        FACADE PATTERN
        Checks if there are any transactions in the current session available for refund.
        """
        session = self.core.sessionManager.getActiveSession()
        return session is not None and len(session.transaction_ids) > 0

    def refundTransaction(self, paymentMethod):
        """
        FACADE PATTERN
        Refunds the last transaction processed by the system.
        """
        print(f" {Colors.CYAN}[INTERFACE]{Colors.RESET} Refund request initiated via {paymentMethod}...")

        command = RefundCommand(paymentMethod)
        return self.core.executeCommand(command)

    """
        Create a restock inventory function to simulate the restock of inventory 
    """
    def restockInventory(self, product, quantity):
        """
            Safety Check :
                If product is not found or quantity is less than or equal to 0, return
        """
        if not product or quantity <= 0:
            print(f"{Colors.ERROR}[INTERFACE ERROR]{Colors.RESET} Invalid input for restock")
            return
        
        print(f"{Colors.CYAN}[INTERFACE]{Colors.RESET} Restock request: {quantity} units")

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
        width = 60
        
        print("\n" + Colors.BLUE + " ╔" + "═"*(width-2) + "╗" + Colors.RESET)
        title_text = pad_ansi(Colors.BOLD + Colors.CYAN + "❖ SYSTEM DIAGNOSTICS ENGINE" + Colors.RESET, width-2, 'center')
        print(f" {Colors.BLUE}║{title_text}{Colors.BLUE}║{Colors.RESET}")
        print(Colors.BLUE + " ╠" + "═"*(width-2) + "╣" + Colors.RESET)
        
        # 1. Render Core Section
        core_data = data["CORE"]
        status_color = Colors.SUCCESS if core_data["AuraCore Integrity"] == "ACTIVE" else Colors.ERROR
        
        lines = [
            f"{Colors.BOLD}AURACORE INTEGRITY:{Colors.RESET}",
            f" > Status:      {status_color}{core_data['AuraCore Integrity']}{Colors.RESET}",
            f" > Personality: {Colors.TEXT}{core_data['Kiosk Personality']}{Colors.RESET}",
            f" > Activity:    {Colors.DIM}{core_data['Activity Ledger']}{Colors.RESET}"
        ]
        
        for line in lines:
            content = pad_ansi("  " + line, width-2, 'left')
            print(f" {Colors.BLUE}║{content}{Colors.BLUE}║{Colors.RESET}")
        
        # 2. Render Inventory Section
        inv = data["INVENTORY"]
        print(Colors.BLUE + " ╟" + "─"*(width-2) + "╢" + Colors.RESET)
        lines = [
            f"{Colors.BOLD}INVENTORY HEALTH:{Colors.RESET}",
            f" > Managed SKUs:  {Colors.HEADER}{inv['Managed SKUs']}{Colors.RESET}",
            f" > Total Stock:   {Colors.TEXT}{inv['Total Stock']}{Colors.RESET}",
            f" > Health Status: {Colors.SUCCESS if inv['Status'] == 'OPTIMIZED' else Colors.WARNING}{inv['Status']}{Colors.RESET}"
        ]
        for line in lines:
            content = pad_ansi("  " + line, width-2, 'left')
            print(f" {Colors.BLUE}║{content}{Colors.BLUE}║{Colors.RESET}")

        # 3. Render Hardware Section
        hw = data["HARDWARE"]
        print(Colors.BLUE + " ╟" + "─"*(width-2) + "╢" + Colors.RESET)
        lines = [
            f"{Colors.BOLD}HARDWARE STACK:{Colors.RESET}",
            f" > Dispense Node: {Colors.HEADER}{hw['Dispensing Node']}{Colors.RESET}",
            f" > Kinetic Drive: {Colors.DIM}{hw['Kiosk Motor Module']}{Colors.RESET}",
            f" > Added Modules: {Colors.CYAN}{hw['Modules Added']}{Colors.RESET}"
        ]
        for line in lines:
            content = pad_ansi("  " + line, width-2, 'left')
            print(f" {Colors.BLUE}║{content}{Colors.BLUE}║{Colors.RESET}")
        
        # 4. Render Extensions Section (if any)
        ext = data["EXTENSIONS"]
        if ext:
            print(Colors.BLUE + " ╟" + "─"*(width-2) + "╢" + Colors.RESET)
            print(f" {Colors.BLUE}║{pad_ansi('  ' + Colors.BOLD + 'ACTIVE EXTENSIONS:', width-2)}{Colors.BLUE}║{Colors.RESET}")
            for key, val in ext.items():
                content = f"   + {key.upper():<12} {Colors.SUCCESS}{val}{Colors.RESET}"
                print(f" {Colors.BLUE}║{pad_ansi('  ' + content, width-2)}{Colors.BLUE}║{Colors.RESET}")
        
        print(Colors.BLUE + " ╚" + "═"*(width-2) + "╝" + Colors.RESET)
        
        # Fetch alerts from Monitoring System
        try:
            from monitoring.monitoring_system import MonitoringSystem
            MonitoringSystem.showAlerts()
        except ImportError:
            pass
            
        return True