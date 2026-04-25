from .inventoryComponent import InventoryComponent

class InventorySystem:
    """
    Proxy Pattern - Real Subject
    Manages the core inventory logic independently, holding a dictionary of InventoryComponents.
    """
    def __init__(self):
        self._items = {}

    def addProduct(self, name: str, item: InventoryComponent):
        self._items[name] = item

    def getProduct(self, name: str) -> InventoryComponent:
        return self._items.get(name)

    def findKeyForProduct(self, product: InventoryComponent) -> str:
        """ Reverse lookup: find the key for a given product object """
        for key, item in self._items.items():
            if item == product:
                return key
        return None

    def getAvailableStock(self, name: str) -> int:
        item = self.getProduct(name)
        if item:
            return item.getAvailableStock()
        return 0

    def reduceStock(self, name: str, qty: int):
        item = self.getProduct(name)
        if not item:
            raise Exception(f"Product {name} not found in inventory.")
        item.reduceStock(qty)

    def addStock(self, name: str, qty: int):
        item = self.getProduct(name)
        if not item:
            raise Exception(f"Product {name} not found in inventory.")
        
        # We need to be able to call addStock, but only SimpleProduct typically has it.
        if hasattr(item, 'addStock'):
            item.addStock(qty)
        else:
            raise Exception(f"Cannot directly add stock to composite grouping {name}.")

    def showAll(self):
        if not self._items:
            print("Inventory is empty.")
            return
        
        print("===== Inventory =====")
        for item in self._items.values():
            item.display()
        print("=====================")