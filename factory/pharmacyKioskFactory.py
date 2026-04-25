from .kioskFactory import KioskFactory
from hardware.dispensers.roboticDispenser import RoboticDispenser

class PharmacyKioskFactory(KioskFactory):
    """
    Concrete Factory for Medical/Pharmacy Kiosks.
    Uses Robotic arms for precise handling of medication.
    """
    
    def createDispenser(self):
        return RoboticDispenser()

    def getKioskType(self):
        return "Aura Medical Pharmacy Kiosk"

    def getDefaultInventory(self):
        return {
            "products": {
                "aspirin": {"id": "M001", "name": "Aspirin 75mg (14s)", "price": 85.0, "stock": 20},
                "bandage": {"id": "M002", "name": "Elastic Crepe Bandage", "price": 120.0, "stock": 15},
                "antiseptic": {"id": "M003", "name": "Antiseptic Spray 50ml", "price": 250.0, "stock": 10},
                "sanitizer": {"id": "M004", "name": "Instant Hand Sanitizer", "price": 60.0, "stock": 40},
                "masks": {"id": "M005", "name": "N95 Medical Masks (3s)", "price": 180.0, "stock": 25},
                "thermometer": {"id": "M006", "name": "Digital Thermometer", "price": 450.0, "stock": 5}
            },
            "bundles": {
                "first_aid": {"name": "Basic First Aid Kit", "discount": 0.10, "items": ["bandage", "antiseptic", "sanitizer"]}
            }
        }
