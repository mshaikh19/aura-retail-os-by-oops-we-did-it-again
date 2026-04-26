from models.session import Session
from persistence.persistenceLayer import PersistentLayer
from utils.colors import Colors

class SessionManager:
    """
    Singleton Pattern
    Manages the active session lifecycle and ensures data persistence.
    """
    _instance = None
    _active_session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print(f" {Colors.HEADER}◈ {Colors.BOLD}SESSION:{Colors.RESET} {Colors.TEXT}Manager initialized.{Colors.RESET}")
        return cls._instance

    def startSession(self, kiosk_id, user_role="CUSTOMER"):
        """ Initialize a new session """
        if self._active_session:
            self.endSession()
            
        self._active_session = Session(kiosk_id, user_role)
        PersistentLayer.saveSession(self._active_session.toDict())
        
        print(f"{Colors.HEADER}[SESSION]{Colors.RESET} New session started: {Colors.CYAN}{self._active_session.session_id[:8]}...{Colors.RESET}")
        return self._active_session

    def getActiveSession(self):
        """ Returns the currently active session """
        return self._active_session

    def linkTransaction(self, transaction_id, amount):
        """ Links a completed transaction to the active session """
        if self._active_session:
            self._active_session.addTransaction(transaction_id, amount)
            PersistentLayer.saveSession(self._active_session.toDict())
            print(f"{Colors.HEADER}[SESSION]{Colors.RESET} Transaction {transaction_id[:8]} linked to session.")

    def endSession(self):
        """ Ends the current session and persists final state """
        if self._active_session:
            sid = self._active_session.session_id[:8]
            self._active_session.endSession()
            PersistentLayer.saveSession(self._active_session.toDict())
            self._active_session = None
            print(f"{Colors.HEADER}[SESSION]{Colors.RESET} Session {Colors.CYAN}{sid}{Colors.RESET} closed successfully.")
