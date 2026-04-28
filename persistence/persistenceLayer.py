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

        with open(file_path, "w") as file:
            json.dump(data_dict, file, indent=4)

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
            if isinstance(v, (str, int, float, bool, list, dict, type(None))):
                serializable_config[k] = v
        
        PersistentLayer.save("config.json", serializable_config)

    @staticmethod
    def loadConfig():
        """
        Load system configuration
        """
        return PersistentLayer.load("config.json")