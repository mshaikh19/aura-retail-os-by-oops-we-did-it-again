from .kioskFactory import KioskFactory
from hardware.dispensers.spiralDispenser import SpiralDispenser

class FoodKioskFactory(KioskFactory):
    """
    Concrete Factory for Food/Vending Kiosks.
    Uses Spiral (Coil) mechanism for dispensing snacks and drinks.
    """
    
    def createDispenser(self):
        return SpiralDispenser()

    def getKioskType(self):
        return "Aura Food & Beverage Kiosk"

    def getDefaultInventory(self):
        return {
            "products": {
                "milk": {"id": "F001", "name": "Milk (500ml)", "price": 55.0, "stock": 15},
                "chips": {"id": "F002", "name": "Classic Potato Chips", "price": 25.0, "stock": 30},
                "cola": {"id": "F003", "name": "Classic Cola 300ml", "price": 40.0, "stock": 25},
                "bread": {"id": "F004", "name": "Multi-Grain Bread", "price": 45.0, "stock": 10},
                "water": {"id": "F005", "name": "Mineral Water 1L", "price": 20.0, "stock": 50},
                "biscuit": {"id": "F006", "name": "Digestive Biscuits", "price": 35.0, "stock": 20}
            },
            "bundles": {
                "snack_pack": {"name": "Snack & Sip Pack", "discount": 0.15, "items": ["chips", "cola"]}
            }
        }
