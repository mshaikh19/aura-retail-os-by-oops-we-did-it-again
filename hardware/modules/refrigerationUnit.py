from .hardwareModule import HardwareModule

class RefrigerationUnit(HardwareModule):
    """
    Concrete Decorator - Adds cooling capabilities to a kiosk.
    """
    
    def __init__(self, wrapped_module=None):
        self._wrapped = wrapped_module
        self._on = False
        self._temp = 4.0 # Target 4 Celsius

    def activate(self):
        self._on = True
        print(f"[FRIDGE] Cooling system engaged. Target: {self._temp}°C")
        if self._wrapped: self._wrapped.activate()

    def deactivate(self):
        self._on = False
        print("[FRIDGE] Cooling system disengaged.")
        if self._wrapped: self._wrapped.deactivate()

    def getStatus(self) -> dict:
        status = {
            "refrigeration": "ACTIVE" if self._on else "OFFLINE",
            "temperature": f"{self._temp}°C" if self._on else "N/A"
        }
        if self._wrapped:
            status.update(self._wrapped.getStatus())
        return status
