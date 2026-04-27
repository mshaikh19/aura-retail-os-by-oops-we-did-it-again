from utils.colors import Colors
from core.sessionManager import SessionManager

class KioskCoreSystem:
    def __init__(self, inventorySystem=None, paymentSystem=None, hardwareSystem=None, kioskType="CORE"):
        #creating subsystems 
        self.inventorySystem = inventorySystem
        self.paymentSystem = paymentSystem
        self.hardwareSystem = hardwareSystem
        self.sessionManager = SessionManager()
        print(f" {Colors.HEADER}◈ {Colors.BOLD}CORE KERNEL:{Colors.RESET} {Colors.TEXT}Aura Retail OS loaded.{Colors.RESET}")

        self.kioskType = kioskType
        self.systemStatus = "ACTIVE"
        self.commandHistory = []
        #keeps track of executed commands
        
        # Decorator management (Hardware Modules)
        self.top_module = None 

    def attachModule(self, module):
        """ Attaches a HardwareModule (Decorator) to the system """
        self.top_module = module
        print(f"{Colors.HEADER}[CORE]{Colors.RESET} Module attached: {type(module).__name__}")
        self.top_module.activate()

    def getModuleStatuses(self):
        """ Returns status of all attached decorators """
        if self.top_module:
            return self.top_module.getStatus()
        return {}

    def getActiveModuleNames(self):
        """ Returns a simple list of active module keys for persistence """
        statuses = self.getModuleStatuses()
        # The status keys usually match the module's core function (e.g., 'refrigeration')
        # We will use this to map back during boot.
        return list(statuses.keys())

    def getOperationalStatus(self):
        """ Comprehensive system health report structured for UI rendering """
        hw_data = self.hardwareSystem.getStatus() if self.hardwareSystem else {}
        
        # Structure the data into logical groups
        report = {
            "CORE": {
                "AuraCore Integrity": self.systemStatus,
                "Kiosk Personality": self.kioskType,
                "Activity Ledger": f"{len(self.commandHistory)} entries"
            },
            "HARDWARE": {
                "Dispensing Node": hw_data.get("dispenser", "OFFLINE"),
                "Kiosk Motor Module": "RUNNING" if hw_data.get("motorRunning") else "IDLE"
            },
            "EXTENSIONS": self.getModuleStatuses()
        }
        return report

    def executeCommand(self, command):

        # 1. Validate command object
        if command is None:
            print(f"{Colors.ERROR}[CORE ERROR]{Colors.RESET} Invalid command.")
            return False

        if not hasattr(command, "execute"):
            print(f"{Colors.ERROR}[CORE ERROR]{Colors.RESET} Command does not implement execute().")
            return False

        # 2. Check system status
        if not self.checkSystemStatus():
            print(f"{Colors.WARNING}[CORE]{Colors.RESET} System not ready. Cannot execute command.")
            return False

        try:
            print(f"\n{Colors.HEADER}[CORE]{Colors.RESET} Executing {command.__class__.__name__}...")

            # 3. Execute command
            result = command.execute(self)

            # 4. Save history
            self.commandHistory.append(command)

            # 5. Session Tracking (Link transaction if applicable)
            if result and self.sessionManager:
                if hasattr(command, 'last_transaction') and command.last_transaction:
                    t = command.last_transaction
                    self.sessionManager.linkTransaction(t.transaction_id, t.total_amount)

            print(f"{Colors.HEADER}[CORE]{Colors.RESET} Command executed successfully.")
            return True

        except Exception as e:
            print(f"{Colors.ERROR}[CORE ERROR]{Colors.RESET} {str(e)}")
            return False

    def checkSystemStatus(self):

        if self.systemStatus == "ERROR":
            print(f"{Colors.ERROR}[CORE ERROR]{Colors.RESET} System in ERROR state.")
            return False

        if self.systemStatus == "EMERGENCY":
            print(f"{Colors.WARNING}[CORE]{Colors.RESET} Emergency mode active. Limited operations.")
            return True

        return True

    def setSystemStatus(self, status):

        validStates = ["ACTIVE", "ERROR", "EMERGENCY"]

        if status in validStates:
            self.systemStatus = status
            print(f"{Colors.HEADER}[CORE]{Colors.RESET} System status changed to {status}")
        else:
            print(f"{Colors.ERROR}[CORE ERROR]{Colors.RESET} Invalid system status.")

    def getSystemStatus(self):
        return self.systemStatus

    def getCommandHistory(self):
        return self.commandHistory