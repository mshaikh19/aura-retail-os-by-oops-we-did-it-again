from hardware.interfaces.dispenserInterface import DispenserInterface
from utils.colors import Colors
import time


class RoboticDispenser(DispenserInterface):
    """
    Simulates high-precision robotic arm movement for pharmaceutical products.
    """

    def dispense(self, product_name, quantity):
        print(f"{Colors.BLUE}[ROBOTIC]{Colors.RESET} Engaging arm → picking {Colors.BOLD}{quantity}x {product_name}{Colors.RESET}")
        time.sleep(0.5)
        return True

    def calibrate(self):
        print("[ROBOT] Calibrating arm joints...")
        return True

    def getStatus(self):
        return "ROBOT_READY"