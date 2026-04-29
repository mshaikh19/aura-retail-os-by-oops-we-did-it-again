import json
import os


class PersistentLayer:
    """
    Central persistence layer for saving and loading system data.
    Stores all data inside the 'data/' folder.
    """

    BASE_PATH = "data"

    @staticmethod
    def _getFilePath(filename):
        return os.path.join(PersistentLayer.BASE_PATH, filename)

    @staticmethod
    def save(filename, data_dict):
        """
        Save any dictionary to a JSON file.
        """
        file_path = PersistentLayer._getFilePath(filename)

        # Ensure data folder exists
        os.makedirs(PersistentLayer.BASE_PATH, exist_ok=True)

        def json_serial(obj):
            """JSON serializer for objects not serializable by default json code"""
            return str(obj)

        with open(file_path, "w") as file:
            json.dump(data_dict, file, indent=4, default=json_serial)

    @staticmethod
    def load(filename):
        """
        Load JSON data from file.
        """
        file_path = PersistentLayer._getFilePath(filename)

        if not os.path.exists(file_path):
            return {}

        with open(file_path, "r") as file:
            try:
                return json.load(file)
            except:
                return {}

    # ---------------- TRANSACTION ---------------- #

    @staticmethod
    def saveTransaction(transaction_dict):
        """
        Append a transaction to transactions.json
        """
        file_path = PersistentLayer._getFilePath("transactions.json")

        # Ensure data folder exists
        os.makedirs(PersistentLayer.BASE_PATH, exist_ok=True)

        transactions = []

        # Load existing transactions
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    transactions = json.load(file)
                except:
                    transactions = []

        # Add new transaction
        transactions.append(transaction_dict)

        # Save back
        with open(file_path, "w") as file:
            json.dump(transactions, file, indent=4)

    @staticmethod
    def loadTransactions():
        """
        Load all transactions from transactions.json
        """
        file_path = PersistentLayer._getFilePath("transactions.json")
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as file:
            try:
                return json.load(file)
            except:
                return []

    # ---------------- INVENTORY ---------------- #

    @staticmethod
    def saveInventoryState(items_dict, filename="inventory.json"):
        """
        Save inventory state
        """
        PersistentLayer.save(filename, items_dict)

    @staticmethod
    def loadInventoryState(filename="inventory.json"):
        """
        Load inventory state
        """
        return PersistentLayer.load(filename)

    @staticmethod
    def loadInventory(inventory_system, filename):
        """ Specialized loader for the inventory system """
        from inventory.components.simpleProduct import SimpleProduct
        from models.productModel import ProductModel
        from inventory.components.productBundle import ProductBundle

        file_path = PersistentLayer._getFilePath(filename)
        if not os.path.exists(file_path):
            return False
            
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                
            # Clear existing
            inventory_system._items = {}
            
            for k, p in data.get("products", {}).items():
                inventory_system.addProduct(
                    k,
                    SimpleProduct(
                        ProductModel(
                            p["product_id"],
                            p["name"],
                            p["price"],
                            p["stock"],
                            p.get("required_module")
                        )
                    )
                )
            
            for k, b in data.get("bundles", {}).items():
                bundle = ProductBundle(b["name"], b["discount"])
                for item_key in b["items"]:
                    prod = inventory_system.getProduct(item_key)
                    if not prod:
                        # Backward compatibility: older files stored product names instead of keys.
                        norm = str(item_key).strip().lower()
                        for candidate in inventory_system._items.values():
                            if hasattr(candidate, "model") and getattr(candidate.model, "name", "").strip().lower() == norm:
                                prod = candidate
                                break
                    if prod:
                        bundle.add(prod)
                inventory_system.addProduct(k, bundle)
            return True
        except Exception:
            return False

    @staticmethod
    def saveInventory(items, filename):
        """ Specialized saver for the inventory system """
        from inventory.components.simpleProduct import SimpleProduct
        from inventory.components.productBundle import ProductBundle

        data = {"products": {}, "bundles": {}}
        for k, item in items.items():
            if isinstance(item, SimpleProduct):
                data["products"][k] = {
                    "product_id": item.model.product_id,
                    "name": item.model.name,
                    "price": item.model.price,
                    "stock": item.model.stock,
                    "required_module": item.model.required_module
                }
            elif isinstance(item, ProductBundle):
                bundle_item_keys = []
                for child in item._items:
                    child_key = None
                    for candidate_key, candidate_item in items.items():
                        if candidate_item is child:
                            child_key = candidate_key
                            break
                    if child_key:
                        bundle_item_keys.append(child_key)

                data["bundles"][k] = {
                    "name": item._name,
                    "discount": item._discount,
                    "items": bundle_item_keys
                }
        
        file_path = PersistentLayer._getFilePath(filename)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    # ---------------- SESSIONS ---------------- #

    @staticmethod
    def saveSession(session_dict):
        """
        Append a session to sessions.json
        """
        file_path = PersistentLayer._getFilePath("sessions.json")
        os.makedirs(PersistentLayer.BASE_PATH, exist_ok=True)

        sessions = []
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    sessions = json.load(file)
                except:
                    sessions = []

        # Check if session already exists (update it) or append
        found = False
        for i, s in enumerate(sessions):
            if s["session_id"] == session_dict["session_id"]:
                sessions[i] = session_dict
                found = True
                break
        
        if not found:
            sessions.append(session_dict)

        with open(file_path, "w") as file:
            json.dump(sessions, file, indent=4)

    @staticmethod
    def loadSessions():
        """
        Load all session data
        """
        file_path = PersistentLayer._getFilePath("sessions.json")
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as file:
            try:
                return json.load(file)
            except:
                return []

    # ---------------- CONFIG ---------------- #

    @staticmethod
    def saveConfig(config_dict):
        """
        Save system configuration. Filters out non-serializable objects
        (like strategy instances) to prevent JSON errors.
        """
        serializable_config = {}
        for k, v in config_dict.items():
            if k == "pricing_policy":
                continue
            if isinstance(v, (str, int, float, bool, list, dict, type(None))):
                serializable_config[k] = v
        
        PersistentLayer.save("config.json", serializable_config)

    @staticmethod
    def loadConfig():
        """
        Load system configuration
        """
        return PersistentLayer.load("config.json")