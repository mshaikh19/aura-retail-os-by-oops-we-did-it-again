from hardware.interfaces.dispenserInterface import DispenserInterface


class ConveyorDispenser(DispenserInterface):
    """
    Simulates conveyor belt (used in bulk/emergency kiosks)
    """

    def dispense(self, product_name, quantity):
        print(f"[CONVEYOR] Belt delivering {quantity}x {product_name}")
        return True

    def calibrate(self):
        print("[CONVEYOR] Calibrating belt speed...")
        return True

    def getStatus(self):
        return "CONVEYOR_READY"