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
        print(f"[CORE] Module attached: {type(module).__name__}")
        self.top_module.activate()

    def getModuleStatuses(self):
        """ Returns status of all attached decorators """
        if self.top_module:
            return self.top_module.getStatus()
        return {}

    def getOperationalStatus(self):
        """ Comprehensive system health report structured for UI rendering """
        hw_data = self.hardwareSystem.getStatus() if self.hardwareSystem else {}
        
        # Structure the data into logical groups
        report = {
            "CORE": {
                "System Status": self.systemStatus,
                "Kiosk Type": self.kioskType,
                "Command Logs": f"{len(self.commandHistory)} executed"
            },
            "HARDWARE": {
                "Dispenser": hw_data.get("dispenser", "OFFLINE"),
                "Motor Module": "RUNNING" if hw_data.get("motorRunning") else "IDLE"
            },
            "EXTENSIONS": self.getModuleStatuses()
        }
        return report

    def executeCommand(self, command):

        # 1. Validate command object
        if command is None:
            print("[CORE] Invalid command.")
            return False

        if not hasattr(command, "execute"):
            print("[CORE] Command does not implement execute().")
            return False

        # 2. Check system status
        if not self.checkSystemStatus():
            print("[CORE] System not ready. Cannot execute command.")
            return False

        try:
            print(f"\n[CORE] Executing {command.__class__.__name__}...")

            # 3. Execute command
            result = command.execute(self)

            # 4. Save history
            self.commandHistory.append(command)

            print("[CORE] Command executed successfully.")
            return True

        except Exception as e:
            print(f"[CORE ERROR] {str(e)}")
            self.systemStatus = "ERROR"
            return False

    def checkSystemStatus(self):

        if self.systemStatus == "ERROR":
            print("[CORE] System in ERROR state.")
            return False

        if self.systemStatus == "EMERGENCY":
            print("[CORE] Emergency mode active. Limited operations.")
            return True

        return True

    def setSystemStatus(self, status):

        validStates = ["ACTIVE", "ERROR", "EMERGENCY"]

        if status in validStates:
            self.systemStatus = status
            print(f"[CORE] System status changed to {status}")
        else:
            print("[CORE] Invalid system status.")

    def getSystemStatus(self):
        return self.systemStatus

    def getCommandHistory(self):
        return self.commandHistory