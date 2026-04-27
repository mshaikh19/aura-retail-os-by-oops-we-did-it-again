from utils.colors import Colors
from inventory.pricing.pricing_policy import StandardPricingPolicy, EmergencyPricingPolicy

class CentralRegistry:
    """
    Singleton Pattern
    Maintains a single global instance for system configuration.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {
                'pricing_policy': StandardPricingPolicy()
            }
            cls._instance._kiosks = {}
            cls._instance._hardware = None
            
            # Machine Presets
            cls._instance.PRESETS = {
                "1": {"label": "Aura Food & Beverage Kiosk", "inventory": "inventory_food.json"},
                "2": {"label": "Aura Medical Pharmacy Kiosk", "inventory": "inventory_pharmacy.json"},
                "3": {"label": "Aura Cyber-Tech Hub", "inventory": "inventory_tech.json"}
            }

            print(f" {Colors.HEADER}* {Colors.BOLD}REGISTRY:{Colors.RESET} {Colors.TEXT}Singleton instance established.{Colors.RESET}")
        return cls._instance

    def registerHardware(self, hardware_ref):
        self._hardware = hardware_ref
        print(f"[REGISTRY] Hardware registered.")

    def getHardware(self):
        return self._hardware


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

    def setPricingPolicy(self, policy):
        self._config['pricing_policy'] = policy
        print(f"[REGISTRY] Pricing policy updated to: {type(policy).__name__}")

    def getPricingPolicy(self):
        if self.getConfig("EMERGENCY_MODE"):
            return EmergencyPricingPolicy()
        return self._config.get('pricing_policy', StandardPricingPolicy())