from hardware.interfaces.dispenserInterface import DispenserInterface


class ConveyorDispenser(DispenserInterface):
    """
    Simulates conveyor belt (used in bulk/emergency kiosks)
    """

    def __init__(self):
        self._jammed_slots = set()

    def dispense(self, product_name, quantity):
        if self.isSlotJammed(product_name):
            print(f"[CONVEYOR ERROR] Belt for {product_name} is JAMMED!")
            return False
        print(f"[CONVEYOR] Belt delivering {quantity}x {product_name}")
        return True

    def calibrate(self):
        print("[CONVEYOR] Calibrating belt speed...")
        return True

    def getStatus(self):
        if self._jammed_slots:
            return f"CONVEYOR_WARNING: {len(self._jammed_slots)} belts jammed"
        return "CONVEYOR_READY"

    def isSlotJammed(self, product_name: str) -> bool:
        return product_name.lower() in self._jammed_slots

    def toggleJam(self, product_name: str):
        name = product_name.lower()
        if name in self._jammed_slots:
            self._jammed_slots.remove(name)
            print(f"[CONVEYOR] Belt for {product_name} UNJAMMED")
        else:
            self._jammed_slots.add(name)
            print(f"[CONVEYOR] Belt for {product_name} JAMMED")