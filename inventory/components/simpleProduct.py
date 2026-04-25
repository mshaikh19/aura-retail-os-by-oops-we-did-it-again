#This class achieves Abstraction, Encapsulation, and SOC(Separation of Concerns)

from .inventoryComponent import InventoryComponent
from models.productModel import ProductModel

class SimpleProduct(InventoryComponent):

    def __init__(self, model: ProductModel):
        self.model = model

    def getStock(self):
        return self.model.stock

    def getAvailableStock(self):
        return self.model.stock

    def isAvailable(self):
        return self.model.stock > 0

    def reduceStock(self, qty):
        if qty <= 0:
            raise ValueError("Quantity must be positive")

        if qty > self.model.stock:
            raise Exception(f"Not enough stock for {self.model.name}")

        self.model.stock -= qty
    
    def addStock(self, qty):
        if qty <= 0:
            raise ValueError("Quantity must be positive")

        self.model.stock += qty

    def getPrice(self):
        return self.model.price

    def getName(self):
        return self.model.name

    def display(self, indent=0):
        print("  " * indent + f"[Product] {self.model.name}  Rs.{self.model.price}  Stock={self.model.stock}")

    def __repr__(self):
        return f"SimpleProduct({self.model.name}, Stock={self.model.stock})"