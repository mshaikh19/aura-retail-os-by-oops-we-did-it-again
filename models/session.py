import uuid
from datetime import datetime

class Session:
    """
    Represents a single user session at the kiosk.
    Tracks the duration and all activities performed.
    """
    def __init__(self, kiosk_id, user_role="CUSTOMER"):
        self.session_id = str(uuid.uuid4())
        self.kiosk_id = kiosk_id
        self.user_role = user_role
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = None
        self.transaction_ids = []
        self.total_spent = 0.0
        self.status = "ACTIVE"

    def addTransaction(self, transaction_id, amount):
        """ Link a transaction to this session """
        self.transaction_ids.append(transaction_id)
        self.total_spent += amount

    def endSession(self):
        """ Mark the session as completed """
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "COMPLETED"

    def toDict(self):
        """ Convert session object to dictionary for persistence """
        return {
            "session_id": self.session_id,
            "kiosk_id": self.kiosk_id,
            "user_role": self.user_role,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "transaction_ids": self.transaction_ids,
            "total_spent": self.total_spent,
            "status": self.status
        }

    @classmethod
    def fromDict(cls, data):
        """ Reconstruct a session object from dictionary data """
        s = cls(data.get("kiosk_id"), data.get("user_role"))
        s.session_id = data.get("session_id", s.session_id)
        s.start_time = data.get("start_time", s.start_time)
        s.end_time = data.get("end_time")
        s.transaction_ids = data.get("transaction_ids", [])
        s.total_spent = data.get("total_spent", 0.0)
        s.status = data.get("status", "COMPLETED")
        return s
