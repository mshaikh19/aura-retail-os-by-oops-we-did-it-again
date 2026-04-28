from utils.colors import Colors
import time

class SystemBootstrapper:
    """
    ABSTRACTED BOOT KERNEL
    Encapsulates the complex initialization sequence to keep the Main terminal clean.
    """
    @staticmethod
    def bootstrap(factory, inventory_real, registry, payment, monitor, show_progress_func):
        from registry.central_registry import CentralRegistry
        from inventory.components.inventoryManager import InventorySystem
        from monitoring.monitoring_system import MonitoringSystem
        from payment.paymentSystem import PaymentSystem
        from inventory.security.inventoryProxy import SecureInventoryProxy
        from hardware.interfaces.hardwareAbstraction import HardwareAbstraction
        from core.kioskCoreSystem import KioskCoreSystem
        from core.kioskInterface import KioskInterface
        from persistence.persistenceLayer import PersistentLayer
        from hardware.modules.solarModule import SolarModule
        from hardware.modules.networkModule import NetworkModule
        from hardware.modules.refrigerationUnit import RefrigerationUnit
        from models.productModel import ProductModel
        from inventory.components.simpleProduct import SimpleProduct
        from inventory.components.productBundle import ProductBundle

        def full_init():
            # 1. Global Core Initialization (Lazy Load)
            reg = registry if registry else CentralRegistry()
            inv = inventory_real if inventory_real else InventorySystem()
            mon = monitor if monitor else MonitoringSystem()
            pay = payment if payment else PaymentSystem()

            # 2. Catalog Sync (Silent)
            kiosk_type = factory.getKioskType()
            inventory_file = "inventory_food.json"
            if "Pharmacy" in kiosk_type: inventory_file = "inventory_pharmacy.json"
            if "Tech" in kiosk_type: inventory_file = "inventory_tech.json"

            if not PersistentLayer.loadInventory(inv, inventory_file):
                data = factory.getDefaultInventory()
                for k, p in data["products"].items():
                    inv.addProduct(k, SimpleProduct(ProductModel(p["id"], p["name"], p["price"], p["stock"])))
                for k, b in data["bundles"].items():
                    bundle = ProductBundle(b["name"], b["discount"])
                    for item_key in b["items"]:
                        prod = inv.getProduct(item_key)
                        if prod: bundle.add(prod)
                    inv.addProduct(k, bundle)
                PersistentLayer.saveInventory(inv._items, inventory_file)

            mon.notify("BOOT", "STORAGE_SYNC", f"Synchronized {inventory_file}")
            
            # 3. Setup Proxy
            proxy = SecureInventoryProxy(
                inv, 
                monitor=mon,
                on_change=lambda: PersistentLayer.saveInventory(inv._items, inventory_file)
            )
            
            # 4. Hardware HAL
            dispenser = factory.createDispenser()
            hardware = HardwareAbstraction(dispenser)
            reg.registerHardware(hardware)
            
            # 5. Core Assembly
            core = KioskCoreSystem(
                inventorySystem=proxy,
                paymentSystem=pay,
                hardwareSystem=hardware,
                kioskType=kiosk_type
            )
            
            # 6. Config Restore
            saved_config = PersistentLayer.loadConfig()
            if saved_config: reg._config.update(saved_config)
            
            # 7. Identity & Session
            reg.setConfig("KIOSK_ID", "AURA-001")
            reg.setConfig("TYPE", kiosk_type)
            reg.registerKiosk("AURA-001", core)
            core.sessionManager.startSession(kiosk_id="AURA-001")
            
            # 8. Hardware Modules
            saved_modules = reg.getConfig("ACTIVE_MODULES") or []
            for mod_name in saved_modules:
                if mod_name == "refrigeration": core.attachModule(RefrigerationUnit(core.top_module))
                elif mod_name == "solar": core.attachModule(SolarModule(core.top_module))
                elif mod_name == "network": core.attachModule(NetworkModule(core.top_module))
            
            # 9. Facade
            interface = KioskInterface(core)
            core.performInitialScan()
            
            return interface, core, inv, mon, reg, pay

        # Show only ONE high-level progress bar to the user
        return show_progress_func("Deploying Aura Environment", full_init)
