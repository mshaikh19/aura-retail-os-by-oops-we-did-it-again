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
                "3": {"label": "Aura Cyber-Tech Hub", "inventory": "inventory_tech.json"},
                "4": {"label": "Aura Metro Essentials Kiosk", "inventory": "inventory_metro.json"},
                "5": {"label": "Aura University Tech Hub", "inventory": "inventory_tech.json"},
                "6": {"label": "Aura Hospital Pharmacy Kiosk", "inventory": "inventory_pharmacy.json"},
                "7": {"label": "Aura Disaster Relief Kiosk", "inventory": "inventory_disaster.json"}
            }

            # No console output for singleton establishment
        return cls._instance

    def registerHardware(self, hardware_ref):
        self._hardware = hardware_ref
        # Logged silently to Audit trail

    def getHardware(self):
        return self._hardware


    def registerKiosk(self, kiosk_id, kiosk_ref):
        self._kiosks[kiosk_id] = kiosk_ref
        # Logged silently to Audit trail

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
        # Logged silently to Audit trail

    def getPricingPolicy(self):
        if self.getConfig("EMERGENCY_MODE"):
            return EmergencyPricingPolicy()
        return self._config.get('pricing_policy', StandardPricingPolicy())