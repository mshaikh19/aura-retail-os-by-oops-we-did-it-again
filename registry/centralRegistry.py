from utils.colors import Colors

class CentralRegistry:
    """
    Singleton Pattern
    Maintains a single global instance for system configuration.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {}
            cls._instance._kiosks = {}
            print(f" {Colors.HEADER}◈ {Colors.BOLD}REGISTRY:{Colors.RESET} {Colors.TEXT}Singleton instance established.{Colors.RESET}")
        return cls._instance

    def registerKiosk(self, kiosk_id, kiosk_ref):
        self._kiosks[kiosk_id] = kiosk_ref
        print(f"[REGISTRY] Kiosk registered: {kiosk_id}")

    def getKiosk(self, kiosk_id):
        return self._kiosks.get(kiosk_id)

    def listKiosks(self):
        return list(self._kiosks.keys())

    def setConfig(self, key, value):
        self._config[key] = value

    def getConfig(self, key):
        return self._config.get(key)
