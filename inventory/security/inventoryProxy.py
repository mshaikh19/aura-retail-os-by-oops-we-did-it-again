from datetime import datetime

class SecureInventoryProxy:
    """
    Proxy Pattern - Security Proxy
    Sits in front of InventorySystem. Every operation is logged. Role checks prevent unauthorized access.
    """
    def __init__(self, inventory_system, role="STAFF", monitor=None, on_change=None):
        self._inventory_system = inventory_system
        self._role = role
        self._access_log = []
        self._monitor = monitor  # Optional MonitoringSystem instance injected
        self._on_change = on_change # Callback for persistence synchronization

    def _log(self, action: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{self._role}] {action}"
        self._access_log.append(log_entry)

    def _checkRole(self, required="STAFF"):
        # For our purposes, STAFF or ADMIN can perform these actions
        if self._role != required and self._role != "ADMIN":
            raise PermissionError(f"Access denied. Required role: {required}")

    def getProduct(self, name: str):
        self._log("READ")
        self._checkRole(required="STAFF")
        return self._inventory_system.getProduct(name)

    def findKeyForProduct(self, product):
        """ Delegate key lookup to the real inventory system """
        return self._inventory_system.findKeyForProduct(product)

    def reduceStock(self, name: str, qty: int):
        self._log("REDUCE")
        self._checkRole(required="STAFF")
        
        self._inventory_system.reduceStock(name, qty)
        
        # Trigger persistence sync if callback exists
        if self._on_change:
            self._on_change()

        current_stock = self._inventory_system.getAvailableStock(name)
        if current_stock < 3:
            if self._monitor:
                self._monitor.notify(source="SecureInventoryProxy", event_type="LOW_STOCK", detail=f"{name} stock drops to {current_stock}")
            else:
                print(f"[SYSTEM EVENT FIRED] LOW_STOCK on {name} (Current: {current_stock})")

    def addStock(self, name: str, qty: int):
        self._log("RESTOCK")
        self._checkRole(required="STAFF")
        self._inventory_system.addStock(name, qty)
        
        # Trigger persistence sync if callback exists
        if self._on_change:
            self._on_change()

    def showAll(self):
        self._log("VIEW ALL")
        self._inventory_system.showAll()

    def getAccessLog(self):
        return self._access_log