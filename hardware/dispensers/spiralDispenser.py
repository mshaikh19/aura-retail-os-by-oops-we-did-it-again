from hardware.interfaces.dispenserInterface import DispenserInterface


class SpiralDispenser(DispenserInterface):
    """
    Simulates spiral coil mechanism (like snack vending machines)
    """

    def dispense(self, product_name, quantity):
        print(f"[SPIRAL] Rotating coil → dispensing {quantity}x {product_name}")
        return True

    def calibrate(self):
        print("[SPIRAL] Calibrating motor...")
        return True

    def getStatus(self):
        return "SPIRAL_READY"