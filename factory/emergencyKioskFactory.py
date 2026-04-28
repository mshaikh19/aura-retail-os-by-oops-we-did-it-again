from .kioskFactory import KioskFactory
from hardware.dispensers.conveyorDispenser import ConveyorDispenser
from utils.colors import Colors

class EmergencyKioskFactory(KioskFactory):
    def __init__(self):
        print(f" {Colors.SUCCESS}◈ {Colors.BOLD}FACTORY:{Colors.RESET} {Colors.TEXT}Disaster Relief Blueprint selected.{Colors.RESET}")

    def createDispenser(self):
        # Conveyor is robust for bulk/emergency distribution
        return ConveyorDispenser()

    def getKioskType(self):
        return "Aura Disaster Relief Kiosk"

    def getDefaultInventory(self):
        return {
            "products": {
                "water": {"id": "D001", "name": "Bottled Water 1L", "price": 20.0, "stock": 200},
                "first_aid": {"id": "D002", "name": "First Aid Kit", "price": 350.0, "stock": 100},
                "blanket": {"id": "D003", "name": "Thermal Blanket", "price": 150.0, "stock": 150},
                "battery": {"id": "D004", "name": "AA Battery Pack (4)", "price": 120.0, "stock": 300},
                "mask": {"id": "D005", "name": "N95 Mask (5s)", "price": 250.0, "stock": 200},
                "sanitizer": {"id": "D006", "name": "Hand Sanitizer 500ml", "price": 180.0, "stock": 150}
            },
            "bundles": {
                "relief_pack": {"name": "Emergency Relief Pack", "discount": 0.25, "items": ["water", "first_aid", "blanket"]}
            }
        }
