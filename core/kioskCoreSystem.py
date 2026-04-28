from utils.colors import Colors
from core.sessionManager import SessionManager
import time
import threading

class KioskCoreSystem:
    def __init__(self, inventorySystem=None, paymentSystem=None, hardwareSystem=None, kioskType="CORE"):
        #creating subsystems 
        from monitoring.monitoringSystem import MonitoringSystem
        self.inventorySystem = inventorySystem
        self.paymentSystem = paymentSystem
        self.hardwareSystem = hardwareSystem
        self.sessionManager = SessionManager()
        
        # Log to secure audit trail, don't clutter customer screen
        MonitoringSystem.notify(source="CORE", event_type="KERNEL_LOAD", detail="Aura Retail OS Kernel successfully initialized.")

        self.kioskType = kioskType
        self.systemStatus = "ACTIVE"
        self.commandHistory = []
        # Simple counter for active in-flight commands to support safe hot-swap
        self._active_commands = 0
        #keeps track of executed commands
        
        # Decorator management (Hardware Modules)
        self.top_module = None 

    def attachModule(self, module):
        """ Attaches a HardwareModule (Decorator) to the system """
        from monitoring.monitoringSystem import MonitoringSystem
        self.top_module = module
        mod_name = type(module).__name__
        # Logged silently to Audit trail
        MonitoringSystem.notify(source="CORE", event_type="MODULE_ATTACHED", detail=f"New hardware extension added: {mod_name}")
        self.top_module.activate()

    def performInitialScan(self):
        """ Performs a boot-time health check to log pre-existing alerts """
        from monitoring.monitoringSystem import MonitoringSystem
        
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
            # mark active command
            self._active_commands += 1

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
        finally:
            # decrement active counter in all cases
            try:
                self._active_commands = max(0, self._active_commands - 1)
            except Exception:
                self._active_commands = 0

    def checkSystemStatus(self):

        if self.systemStatus == "ERROR":
            print(f"{Colors.ERROR}[CORE ERROR]{Colors.RESET} System in ERROR state.")
            return False

        if self.systemStatus == "MAINTENANCE":
            print(f"{Colors.WARNING}[CORE]{Colors.RESET} Maintenance mode active. Operations paused.")
            return False

        if self.systemStatus == "EMERGENCY":
            print(f"{Colors.WARNING}[CORE]{Colors.RESET} Emergency mode active. Limited operations.")
            return True

        return True

    def setSystemStatus(self, status):

        validStates = ["ACTIVE", "ERROR", "EMERGENCY", "MAINTENANCE"]

        if status in validStates:
            self.systemStatus = status
            # Status change logged to memory
        else:
            print(f"{Colors.ERROR}[CORE ERROR]{Colors.RESET} Invalid system status.")

    def getSystemStatus(self):
        return self.systemStatus

    def getCommandHistory(self):
        return self.commandHistory

    # ---------------- HOT-SWAP SUPPORT ---------------- #
    def replaceDispenser(self, new_dispenser, timeout: float = 5.0) -> bool:
        """Safely replace the dispenser at runtime.

        Steps:
        1. Put system into MAINTENANCE to prevent new operations.
        2. Wait for in-flight commands to finish or until timeout.
        3. Swap dispenser on hardwareSystem.
        4. Restore previous system state.
        Returns True on success, False on timeout/failure.
        """
        from monitoring.monitoringSystem import MonitoringSystem

        prev_status = self.systemStatus
        self.setSystemStatus("MAINTENANCE")

        start = time.time()
        while self._active_commands > 0 and (time.time() - start) < timeout:
            time.sleep(0.05)

        if self._active_commands > 0:
            MonitoringSystem.notify(source="CORE", event_type="HOTSWAP_FAILED", detail="Timeout waiting for active commands to finish")
            # restore previous status
            self.setSystemStatus(prev_status)
            return False

        # perform swap
        try:
            if self.hardwareSystem:
                self.hardwareSystem.swapDispenser(new_dispenser)
                MonitoringSystem.notify(source="CORE", event_type="HOTSWAP_SUCCESS", detail=f"Dispenser swapped to {new_dispenser.__class__.__name__}")
            else:
                MonitoringSystem.notify(source="CORE", event_type="HOTSWAP_FAILED", detail="No hardware system present")
                self.setSystemStatus(prev_status)
                return False
        finally:
            # restore previous status
            self.setSystemStatus(prev_status)

        return True