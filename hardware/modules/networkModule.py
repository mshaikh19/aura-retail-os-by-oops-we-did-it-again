from .hardwareModule import HardwareModule

class NetworkModule(HardwareModule):
    """
    Concrete Decorator - Adds 5G/Network connectivity to a kiosk.
    """
    
    def __init__(self, wrapped_module=None):
        self._wrapped = wrapped_module
        self._connected = False
        self._signal = 0

    def activate(self):
        self._connected = True
        self._signal = 98 # 98% Signal
        print(f"[NETWORK] Link established. Signal strength: {self._signal}%")
        if self._wrapped: self._wrapped.activate()

    def deactivate(self):
        self._connected = False
        self._signal = 0
        print("[NETWORK] Link severed.")
        if self._wrapped: self._wrapped.deactivate()

    def getStatus(self) -> dict:
        status = {
            "network": "5G_CONNECTED" if self._connected else "OFFLINE",
            "signal": f"{self._signal}%" if self._connected else "0%"
        }
        if self._wrapped:
            status.update(self._wrapped.getStatus())
        return status
