from hardware.interfaces.dispenserInterface import DispenserInterface


class RoboticDispenser(DispenserInterface):
    """
    Simulates robotic arm (used in pharmacy kiosks)
    """

    def __init__(self):
        self._jammed_slots = set()

    def dispense(self, product_name, quantity):
        if self.isSlotJammed(product_name):
            print(f"[ROBOT ERROR] Arm cannot reach slot for {product_name} - OBSTRUCTED!")
            return False
        print(f"[ROBOT] Arm picking {quantity}x {product_name}")
        return True

    def calibrate(self):
        print("[ROBOT] Calibrating arm joints...")
        return True

    def getStatus(self):
        if self._jammed_slots:
            return f"ROBOT_WARNING: {len(self._jammed_slots)} slots obstructed"
        return "ROBOT_READY"

    def isSlotJammed(self, product_name: str) -> bool:
        return product_name.lower() in self._jammed_slots

    def toggleJam(self, product_name: str):
        name = product_name.lower()
        if name in self._jammed_slots:
            self._jammed_slots.remove(name)
            print(f"[ROBOT] Slot for {product_name} OBSTRUCTION CLEARED")
        else:
            self._jammed_slots.add(name)
            print(f"[ROBOT] Slot for {product_name} OBSTRUCTED")