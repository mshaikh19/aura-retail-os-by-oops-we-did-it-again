from hardware.interfaces.dispenserInterface import DispenserInterface


class SpiralDispenser(DispenserInterface):
    """
    Simulates spiral coil mechanism (like snack vending machines)
    """

    def __init__(self):
        self._jammed_slots = set()

    def dispense(self, product_name, quantity):
        if self.isSlotJammed(product_name):
            print(f"[SPIRAL ERROR] Slot for {product_name} is JAMMED!")
            return False
        print(f"[SPIRAL] Rotating coil → dispensing {quantity}x {product_name}")
        return True

    def calibrate(self):
        print("[SPIRAL] Calibrating motor...")
        return True

    def getStatus(self):
        if self._jammed_slots:
            return f"SPIRAL_WARNING: {len(self._jammed_slots)} slots jammed"
        return "SPIRAL_READY"

    def isSlotJammed(self, product_name: str) -> bool:
        return product_name.lower() in self._jammed_slots

    def toggleJam(self, product_name: str):
        name = product_name.lower()
        if name in self._jammed_slots:
            self._jammed_slots.remove(name)
            print(f"[SPIRAL] Slot for {product_name} UNJAMMED")
        else:
            self._jammed_slots.add(name)
            print(f"[SPIRAL] Slot for {product_name} JAMMED")