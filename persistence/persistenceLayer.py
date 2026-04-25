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

    # ---------------- INVENTORY ---------------- #

    @staticmethod
    def saveInventoryState(items_dict):
        """
        Save inventory state
        """
        PersistentLayer.save("inventory.json", items_dict)

    @staticmethod
    def loadInventoryState():
        """
        Load inventory state
        """
        return PersistentLayer.load("inventory.json")

    # ---------------- CONFIG ---------------- #

    @staticmethod
    def saveConfig(config_dict):
        """
        Save system configuration
        """
        PersistentLayer.save("config.json", config_dict)