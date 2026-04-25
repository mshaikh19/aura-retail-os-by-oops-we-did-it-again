from .inventoryComponent import InventoryComponent

class ProductBundle(InventoryComponent):
    """
    Composite Pattern - Composite Node
    Represents a bundle of multiple InventoryComponents.
    """

    def __init__(self, name: str, discount: float = 0.0):
        self._name = name
        self._discount = discount
        self._items = []

    def add(self, item: InventoryComponent):
        self._items.append(item)

    def remove(self, item: InventoryComponent):
        if item in self._items:
            self._items.remove(item)

    def getName(self) -> str:
        return self._name

    def getPrice(self) -> float:
        total_price = sum(item.getPrice() for item in self._items)
        return total_price * (1.0 - self._discount)

    def getAvailableStock(self) -> int:
        if not self._items:
            return 0
        return min(item.getAvailableStock() for item in self._items)

    def reduceStock(self, qty: int):
        if qty <= 0:
            raise ValueError("Quantity must be positive")
            
        if self.getAvailableStock() < qty:
            raise Exception(f"Not enough stock for bundle: {self._name}")
            
        for item in self._items:
            item.reduceStock(qty)

    def isAvailable(self) -> bool:
        if not self._items:
            return False
        return all(item.isAvailable() for item in self._items)

    def display(self, indent=0):
        print("  " * indent + f"[Bundle] {self._name}  Rs.{self.getPrice():.2f} (Discount: {self._discount*100}%)")
        for item in self._items:
            item.display(indent + 2)
