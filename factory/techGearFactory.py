from .kioskFactory import KioskFactory
from hardware.dispensers.conveyorDispenser import ConveyorDispenser

class TechGearFactory(KioskFactory):
    """
    Concrete Factory for Cyber-Tech/Electronics Kiosks.
    Sells high-demand gadgets using a Conveyor Belt system.
    """
    
    def createDispenser(self):
        return ConveyorDispenser()

    def getKioskType(self):
        return "Aura Cyber-Tech Hub"

    def getDefaultInventory(self):
        return {
            "products": {
                "powerbank": {"id": "T001", "name": "Aura 20000mAh PowerBank", "price": 1200.0, "stock": 10},
                "cable": {"id": "T002", "name": "USB-C Braided Cable 2m", "price": 450.0, "stock": 50},
                "earbuds": {"id": "T003", "name": "Aura AirPods Pro", "price": 2500.0, "stock": 8},
                "adapter": {"id": "T004", "name": "65W GaN Charger", "price": 850.0, "stock": 15},
                "ssd": {"id": "T005", "name": "Aura NVMe 1TB Portable", "price": 4500.0, "stock": 5},
                "mouse": {"id": "T006", "name": "RGB Wireless Mouse", "price": 950.0, "stock": 12}
            },
            "bundles": {
                "creator_kit": {"name": "Content Creator Bundle", "discount": 0.20, "items": ["powerbank", "cable", "ssd"]}
            }
        }
