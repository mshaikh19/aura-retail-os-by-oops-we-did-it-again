from .kioskFactory import KioskFactory
from hardware.dispensers.spiralDispenser import SpiralDispenser
from utils.colors import Colors

class MetroKioskFactory(KioskFactory):
    def __init__(self):
        print(f" {Colors.SUCCESS}◈ {Colors.BOLD}FACTORY:{Colors.RESET} {Colors.TEXT}Metro Essentials Blueprint selected.{Colors.RESET}")

    def createDispenser(self):
        return SpiralDispenser()

    def getKioskType(self):
        return "Aura Metro Essentials Kiosk"

    def getDefaultInventory(self):
        return {
            "products": {
                "water": {"id": "M001", "name": "Mineral Water 500ml", "price": 25.0, "stock": 100},
                "snack": {"id": "M002", "name": "On-the-go Snack", "price": 30.0, "stock": 80},
                "umbrella": {"id": "M003", "name": "Compact Umbrella", "price": 199.0, "stock": 20},
                "mask": {"id": "M004", "name": "Disposable Mask (5s)", "price": 50.0, "stock": 60},
                "sanitizer": {"id": "M005", "name": "Hand Sanitizer 100ml", "price": 75.0, "stock": 50},
                "charger": {"id": "M006", "name": "Fast Charger (USB-C)", "price": 399.0, "stock": 25}
            },
            "bundles": {
                "commute_kit": {"name": "Commute Essentials Pack", "discount": 0.12, "items": ["water", "snack", "mask"]}
            }
        }
