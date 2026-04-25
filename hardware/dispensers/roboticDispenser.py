from hardware.interfaces.dispenserInterface import DispenserInterface


class RoboticDispenser(DispenserInterface):
    """
    Simulates robotic arm (used in pharmacy kiosks)
    """

    def dispense(self, product_name, quantity):
        print(f"[ROBOT] Arm picking {quantity}x {product_name}")
        return True

    def calibrate(self):
        print("[ROBOT] Calibrating arm joints...")
        return True

    def getStatus(self):
        return "ROBOT_READY"