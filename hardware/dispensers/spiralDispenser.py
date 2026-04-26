from hardware.interfaces.dispenserInterface import DispenserInterface
from utils.colors import Colors
import time

class SpiralDispenser(DispenserInterface):
    """
    Simulates spiral coil mechanism (like snack vending machines)
    """

    def dispense(self, product_name, quantity):
        print(f"{Colors.BLUE}[SPIRAL]{Colors.RESET} Rotating coil → dispensing {Colors.BOLD}{quantity}x {product_name}{Colors.RESET}")
        time.sleep(0.5)
        return True

    def calibrate(self):
        print("[SPIRAL] Calibrating motor...")
        return True

    def getStatus(self):
        return "SPIRAL_READY"