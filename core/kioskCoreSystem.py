from utils.colors import Colors
from core.sessionManager import SessionManager

class KioskCoreSystem:
    def __init__(self, inventorySystem=None, paymentSystem=None, hardwareSystem=None, kioskType="CORE"):
        #creating subsystems 
        from monitoring.monitoring_system import MonitoringSystem
        self.inventorySystem = inventorySystem
        self.paymentSystem = paymentSystem
        self.hardwareSystem = hardwareSystem
        self.sessionManager = SessionManager()
        
        # Log to secure audit trail, don't clutter customer screen
        MonitoringSystem.notify(source="CORE", event_type="KERNEL_LOAD", detail="Aura Retail OS Kernel successfully initialized.")

        self.kioskType = kioskType
        self.systemStatus = "ACTIVE"
        self.commandHistory = []
        #keeps track of executed commands
        
        # Decorator management (Hardware Modules)
        self.top_module = None 

    def attachModule(self, module):
        """ Attaches a HardwareModule (Decorator) to the system """
        from monitoring.monitoring_system import MonitoringSystem
        self.top_module = module
        mod_name = type(module).__name__
        # Logged silently to Audit trail
        MonitoringSystem.notify(source="CORE", event_type="MODULE_ATTACHED", detail=f"New hardware extension added: {mod_name}")
        self.top_module.activate()

    def performInitialScan(self):
        """ Performs a boot-time health check to log pre-existing alerts """
        from monitoring.monitoring_system import MonitoringSystem
        
        # Check Inventory for pre-existing low stock
        items = self.inventorySystem._inventory_system._items if hasattr(self.inventorySystem, "_inventory_system") else {}
        found_issues = 0
        for name, item in items.items():
            stock = item.getAvailableStock()
            if stock < 5:
                MonitoringSystem.notify(source="BOOT_SCAN", event_type="LOW_STOCK", detail=f"{name.upper()} is critically low ({stock} units)")
                found_issues += 1
        
        # Check for attached modules
        active_mods = self.getActiveModuleNames()
        if active_mods:
             MonitoringSystem.notify(source="BOOT_SCAN", event_type="SYSTEM_READY", detail=f"System online with {len(active_mods)} modules: {', '.join(active_mods)}")
        else:
             MonitoringSystem.notify(source="BOOT_SCAN", event_type="SYSTEM_READY", detail="System online (Standard Configuration)")
             
        # Issues are logged to Sentinel Audit trail, not printed to user
        if found_issues > 0:
             pass

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
        # Calculate Inventory Health
        items = self.inventorySystem._inventory_system._items if hasattr(self.inventorySystem, "_inventory_system") else {}
        total_items = len(items)
        total_stock = sum(item.getAvailableStock() for item in items.values()) if items else 0

        report = {
            "CORE": {
                "AuraCore Integrity": self.systemStatus,
                "Kiosk Personality": self.kioskType,
                "Activity Ledger": f"{len(self.commandHistory)} entries"
            },
            "INVENTORY": {
                "Managed SKUs": total_items,
                "Total Stock": f"{total_stock} units",
                "Status": "OPTIMIZED" if total_stock > 10 else "LOW_STOCK"
            },
            "HARDWARE": {
                "Dispensing Node": hw_data.get("dispenser", "OFFLINE"),
                "Kiosk Motor Module": "RUNNING" if hw_data.get("motorRunning") else "IDLE",
                "Modules Added": ", ".join([m.upper() for m in self.getActiveModuleNames()]) or "NONE"
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
            # 3. Execute command silently
            result = command.execute(self)

            # 4. Save history
            self.commandHistory.append(command)

            # 5. Session Tracking (Link transaction if applicable)
            if result and self.sessionManager:
                if hasattr(command, 'last_transaction') and command.last_transaction:
                    t = command.last_transaction
                    self.sessionManager.linkTransaction(t.transaction_id, t.total_amount)

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
            # Status change logged to memory
        else:
            print(f"{Colors.ERROR}[CORE ERROR]{Colors.RESET} Invalid system status.")

    def getSystemStatus(self):
        return self.systemStatus

    def getCommandHistory(self):
        return self.commandHistory