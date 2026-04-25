from .hardwareModule import HardwareModule

class SolarModule(HardwareModule):
    """
    Concrete Decorator - Adds solar power charging to a kiosk.
    """
    
    def __init__(self, wrapped_module=None):
        self._wrapped = wrapped_module
        self._watts = 0
        self._charging = False

    def activate(self):
        self._charging = True
        self._watts = 150 # Peak output
        print(f"[SOLAR] Panels deployed. Generating {self._watts}W")
        if self._wrapped: self._wrapped.activate()

    def deactivate(self):
        self._charging = False
        self._watts = 0
        print("[SOLAR] Panels stowed.")
        if self._wrapped: self._wrapped.deactivate()

    def getStatus(self) -> dict:
        status = {
            "solar_power": f"{self._watts}W" if self._charging else "0W",
            "charging": "YES" if self._charging else "NO"
        }
        if self._wrapped:
            status.update(self._wrapped.getStatus())
        return status
