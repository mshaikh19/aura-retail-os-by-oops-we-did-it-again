import uuid
from datetime import datetime


class Transaction:
    """
    Represents a single transaction in the system.
    Stores all details related to a purchase or refund.
    """

    def __init__(self, product_name, quantity, total_amount, payment_method, status, kiosk_type="UNKNOWN"):
        """
        Initializes a transaction with all required details.
        """

        # Unique transaction ID
        self.transaction_id = str(uuid.uuid4())

        # Product details
        self.product_name = product_name
        self.quantity = quantity

        # Pricing details
        self.total_amount = total_amount

        # Payment method used (UPI / CARD / WALLET)
        self.payment_method = payment_method

        # Transaction status (SUCCESS / FAILED / REFUNDED)
        self.status = status

        # Kiosk Application Type
        self.kiosk_type = kiosk_type

        # Timestamp of transaction
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def toDict(self):
        """
        Converts transaction object into dictionary format.
        Useful for saving data (JSON/CSV).
        """
        return {
            "transaction_id": self.transaction_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "total_amount": self.total_amount,
            "payment_method": self.payment_method,
            "status": self.status,
            "kiosk_type": self.kiosk_type,
            "timestamp": self.timestamp
        }

    @classmethod
    def fromDict(cls, data):
        """
        Creates a Transaction object from a dictionary.
        """
        t = cls(
            product_name=data.get("product_name"),
            quantity=data.get("quantity"),
            total_amount=data.get("total_amount"),
            payment_method=data.get("payment_method"),
            status=data.get("status"),
            kiosk_type=data.get("kiosk_type", "UNKNOWN")
        )
        t.transaction_id = data.get("transaction_id", t.transaction_id)
        t.timestamp = data.get("timestamp", t.timestamp)
        return t

    def __repr__(self):
        """
        Returns readable string representation of transaction.
        Useful for debugging/logging.
        """
        return (f"Transaction(id={self.transaction_id}, "
                f"product={self.product_name}, qty={self.quantity}, "
                f"amount={self.total_amount}, method={self.payment_method}, "
                f"status={self.status}, time={self.timestamp})")