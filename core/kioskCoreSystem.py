from utils.colors import Colors
import time

class KioskCoreSystem:
    def __init__(self, inventorySystem=None, paymentSystem=None, hardwareSystem=None, kioskType="CORE"):
        #creating subsystems 
        self.inventorySystem = inventorySystem
        self.paymentSystem = paymentSystem
        self.hardwareSystem = hardwareSystem

        self.kioskType = kioskType
        self.systemStatus = "ACTIVE"
        self.commandHistory = []
        #keeps track of executed commands
        
        # Decorator management (Hardware Modules)
        self.top_module = None 

    def attachModule(self, module):
        """ Attaches a HardwareModule (Decorator) to the system """
        self.top_module = module
        print(f"{Colors.HEADER}[CORE]{Colors.RESET} Module attached: {Colors.CYAN}{type(module).__name__}{Colors.RESET}")
        time.sleep(0.3)
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
            print(f"{Colors.ERROR}[CORE] Invalid command.{Colors.RESET}")
            return False

        if not hasattr(command, "execute"):
            print(f"{Colors.ERROR}[CORE] Command does not implement execute().{Colors.RESET}")
            return False

        # 2. Check system status
        if not self.checkSystemStatus():
            print(f"{Colors.ERROR}[CORE] System not ready. Cannot execute command.{Colors.RESET}")
            return False

        try:
            print(f"{Colors.HEADER}[CORE]{Colors.RESET} Executing {Colors.BOLD}{command.__class__.__name__}{Colors.RESET}...")
            time.sleep(0.3)

            # 3. Execute command
            result = command.execute(self)

            # 4. Save history
            self.commandHistory.append(command)

            print(f"{Colors.SUCCESS}[CORE] Command executed successfully.{Colors.RESET}")
            time.sleep(0.3)
            return True

        except Exception as e:
            print(f"{Colors.ERROR}[CORE ERROR] {str(e)}{Colors.RESET}")
            self.systemStatus = "ERROR"
            return False

    def checkSystemStatus(self):

        if self.systemStatus == "ERROR":
            print(f"{Colors.ERROR}[CORE] System in ERROR state.{Colors.RESET}")
            return False

        if self.systemStatus == "EMERGENCY":
            print(f"{Colors.WARNING}[CORE] Emergency mode active. Limited operations.{Colors.RESET}")
            return True

        return True

    def setSystemStatus(self, status):

        validStates = ["ACTIVE", "ERROR", "EMERGENCY"]

        if status in validStates:
            self.systemStatus = status
            print(f"{Colors.HEADER}[CORE]{Colors.RESET} System status changed to {Colors.BOLD}{status}{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}[CORE] Invalid system status.{Colors.RESET}")

    def getSystemStatus(self):
        return self.systemStatus

    def getCommandHistory(self):
        return self.commandHistory