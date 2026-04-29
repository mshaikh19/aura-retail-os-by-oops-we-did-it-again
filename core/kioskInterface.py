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
        from monitoring.monitoringSystem import MonitoringSystem
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

        required_module = getattr(getattr(product, "model", None), "required_module", None)
        if required_module:
            active_modules = [m.lower() for m in (self.core.getActiveModuleNames() or [])]
            if required_module.lower() not in active_modules:
                print(
                    f"{Colors.ERROR}[INTERFACE]{Colors.RESET} {product.getName()} is locked. "
                    f"Requires {required_module.upper()} module before purchase."
                )
                return False

        """
            Process the request
        """
        print(f"{Colors.CYAN}[INTERFACE]{Colors.RESET} Purchase request: {quantity} units")

        """
            Create a command object to pass to the core system for purchasing product
        """
        command = PurchaseCommand(product, quantity, paymentMethod)
        return self.core.executeCommand(command)

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
        width = 80
        indent = " " * 0 # Using relative centering or fixed indent
        
        # Helper to print a centered boxed section
        def print_section(title, lines, is_first=False):
            from utils.ui_utils import pad_ansi
            if is_first:
                print("\n" + Colors.BLUE + " ╔" + "═"*(width-2) + "╗" + Colors.RESET)
                title_text = pad_ansi(Colors.BOLD + Colors.CYAN + title + Colors.RESET, width-2, 'center')
                print(f" {Colors.BLUE}║{title_text}{Colors.BLUE}║{Colors.RESET}")
                print(Colors.BLUE + " ╠" + "═"*(width-2) + "╣" + Colors.RESET)
            else:
                print(Colors.BLUE + " ╟" + "─"*(width-2) + "╢" + Colors.RESET)
                header_text = pad_ansi("  " + Colors.BOLD + title + Colors.RESET, width-2, 'left')
                print(f" {Colors.BLUE}║{header_text}{Colors.BLUE}║{Colors.RESET}")

            for line in lines:
                content = pad_ansi("    " + line, width-2, 'left')
                print(f" {Colors.BLUE}║{content}{Colors.BLUE}║{Colors.RESET}")


        # 1. Render Core Section
        core_data = data["CORE"]
        status_color = Colors.SUCCESS if core_data["AuraCore Integrity"] == "ACTIVE" else Colors.ERROR
        core_lines = [
            f" > Status:      {status_color}{core_data['AuraCore Integrity']}{Colors.RESET}",
            f" > Personality: {Colors.TEXT}{core_data['Kiosk Personality']}{Colors.RESET}",
            f" > Activity:    {Colors.DIM}{core_data['Activity Ledger']}{Colors.RESET}"
        ]
        print_section("❖ SYSTEM DIAGNOSTICS ENGINE", core_lines, is_first=True)
        
        # 2. Render Inventory Section
        inv = data["INVENTORY"]
        inv_lines = [
            f" > Managed SKUs:  {Colors.HEADER}{inv['Managed SKUs']}{Colors.RESET}",
            f" > Total Stock:   {Colors.TEXT}{inv['Total Stock']}{Colors.RESET}",
            f" > Health Status: {Colors.SUCCESS if inv['Status'] == 'OPTIMIZED' else Colors.WARNING}{inv['Status']}{Colors.RESET}"
        ]
        print_section("INVENTORY HEALTH", inv_lines)

        # 3. Render Hardware Section
        hw = data["HARDWARE"]
        hw_lines = [
            f" > Dispense Node: {Colors.HEADER}{hw['Dispensing Node']}{Colors.RESET}",
            f" > Kinetic Drive: {Colors.DIM}{hw['Kiosk Motor Module']}{Colors.RESET}",
            f" > Added Modules: {Colors.CYAN}{hw['Modules Added']}{Colors.RESET}"
        ]
        print_section("HARDWARE STACK", hw_lines)
        
        # 4. Render Extensions Section (if any)
        ext = data["EXTENSIONS"]
        if ext:
            ext_lines = []
            for key, val in ext.items():
                ext_lines.append(f" + {key.upper():<12} {Colors.SUCCESS}{val}{Colors.RESET}")
            print_section("ACTIVE EXTENSIONS", ext_lines)
        
        print(Colors.BLUE + " ╚" + "═"*(width-2) + "╝" + Colors.RESET)

        
        # Fetch alerts from Monitoring System
        try:
            from monitoring.monitoringSystem import MonitoringSystem
            MonitoringSystem.showAlerts()
        except ImportError:
            pass
            
        return True