from hardware.interfaces.dispenserInterface import DispenserInterface
from utils.colors import Colors
import time


class ConveyorDispenser(DispenserInterface):
    """
    Simulates conveyor belt transport for electronic items.
    """

    def dispense(self, product_name, quantity):
        print(f"{Colors.BLUE}[CONVEYOR]{Colors.RESET} Belt active → moving {Colors.BOLD}{quantity}x {product_name}{Colors.RESET}")
        time.sleep(0.5)
        return True

    def calibrate(self):
        print("[CONVEYOR] Calibrating belt speed...")
        return True

    def getStatus(self):
        return "CONVEYOR_READY"