# Import adapter classes for different payment methods
from payment.adapters.upiAdapter import UPIAdapter
from payment.adapters.cardAdapter import CardAdapter
from payment.adapters.walletAdapter import WalletAdapter

# Import Transaction model
from models.transaction import Transaction

# Import Persistent Layer
from persistence.persistenceLayer import PersistentLayer

# Import Monitoring System
from monitoring.monitoring_system import MonitoringSystem

from utils.colors import Colors
from core.sessionManager import SessionManager


class PaymentSystem:

    def __init__(self):
        # Load transaction history from persistent storage
        raw_history = PersistentLayer.loadTransactions()
        self.transactionHistory = []

        for t_dict in raw_history:
            self.transactionHistory.append(Transaction.fromDict(t_dict))

        print(f" {Colors.WARNING}◈ {Colors.BOLD}PAYMENT:{Colors.RESET} {Colors.TEXT}Gateway API initialized ({len(self.transactionHistory)} history entries).{Colors.RESET}")

        # Factory mapping for payment processors
        self.processors = {
            "UPI": UPIAdapter,
            "CARD": CardAdapter,
            "WALLET": WalletAdapter
        }

    # ---------------- PAYMENT ---------------- #

    def makePayment(self, method, amount, product_name=None, quantity=None, kiosk_type="UNKNOWN"):
        print(f"\n{Colors.WARNING}[PAYMENT]{Colors.RESET} Starting payment...")

        processor = self._getProcessor(method)

        if processor is None:
            print(f"{Colors.ERROR}[PAYMENT ERROR]{Colors.RESET} Invalid payment method")
            return False

        # 🔥 UPDATED: adapter returns (success, details)
        success, details = processor.processPayment(amount)

        if success:
            transaction = Transaction(
                product_name=product_name if product_name else "UNKNOWN",
                quantity=quantity if quantity else 0,
                total_amount=amount,
                payment_method=method,
                status="SUCCESS",
                kiosk_type=kiosk_type,
                payment_details=details   # 🔥 store details
            )

            # Store in memory
            self.transactionHistory.append(transaction)

            # Save to JSON
            PersistentLayer.saveTransaction(transaction.toDict())

            # Notify monitoring system
            MonitoringSystem.notify(
                "PAYMENT",
                "TRANSACTION_COMPLETE",
                f"Rs.{amount} via {method}"
            )

            print(f"{Colors.SUCCESS}[PAYMENT]{Colors.RESET} Transaction recorded successfully.")
            print(f"{Colors.WARNING}[PAYMENT]{Colors.RESET} Payment completed")
            return transaction

        print(f"{Colors.ERROR}[PAYMENT]{Colors.RESET} Payment failed")
        return None

    # ---------------- REFUND ---------------- #

    def refund(self, method):
        print(f"\n{Colors.WARNING}[PAYMENT]{Colors.RESET} Starting refund...")

        # BLOCK WALLET REFUND
        if method == "WALLET":
            print(f"{Colors.ERROR}[PAYMENT ERROR]{Colors.RESET} Wallet refunds are not supported")
            return False

        # Get active session
        active_session = SessionManager().getActiveSession()
        if not active_session:
            print(f"{Colors.ERROR}[PAYMENT ERROR]{Colors.RESET} No active session found.")
            return False

        # Filter session transactions that are eligible for refund (not already refunded)
        session_tx_ids = active_session.transaction_ids
        
        # We search from the end of history to find the most recent matching transaction that isn't refunded
        last_transaction = None
        for t in reversed(self.transactionHistory):
            if t.transaction_id in session_tx_ids and t.status != "REFUNDED":
                last_transaction = t
                break
        
        if not last_transaction:
            # Provide specific feedback if transactions exist but are already refunded
            all_session_tx = [t for t in self.transactionHistory if t.transaction_id in session_tx_ids]
            if all_session_tx:
                print(f"{Colors.WARNING}[PAYMENT]{Colors.RESET} All items in this session are already refunded.")
            else:
                print(f"{Colors.WARNING}[PAYMENT]{Colors.RESET} No purchases found in the current session.")
            return False

        processor = self._getProcessor(method)

        if processor is None:
            print(f"{Colors.ERROR}[PAYMENT ERROR]{Colors.RESET} Invalid method")
            return False

        amount = last_transaction.total_amount

        print(f"{Colors.WARNING}[PAYMENT]{Colors.RESET} Refunding Rs.{amount} for {last_transaction.product_name}")

        # smart refund
        original_method = last_transaction.payment_method
        stored_details = last_transaction.payment_details

        # SAME METHOD → reuse details
        if method == original_method:
            print(f"{Colors.CYAN}[PAYMENT]{Colors.RESET} Using stored details: {stored_details}")
            result = processor.refundPayment(amount)

        # DIFFERENT METHOD → re-authenticate
        else:
            print(f"{Colors.WARNING}[PAYMENT]{Colors.RESET} Different method selected. Verification required.")
            
            # reuse adapter input (safe way)
            success, _ = processor.processPayment(0)  # just for input

            if not success:
                print(f"{Colors.ERROR}[PAYMENT]{Colors.RESET} Verification failed")
                return False

            result = processor.refundPayment(amount)

        if result:
            last_transaction.status = "REFUNDED"

            PersistentLayer.saveTransaction(last_transaction.toDict())

            MonitoringSystem.notify(
                "PAYMENT",
                "REFUND_COMPLETE",
                f"Rs.{amount} refunded via {method}"
            )

            print(f"{Colors.SUCCESS}[PAYMENT]{Colors.RESET} Refund successful")

        print(f"{Colors.WARNING}[PAYMENT]{Colors.RESET} Refund completed")
        return result

    # ---------------- HELPER ---------------- #

    def _getProcessor(self, method):
        processor_class = self.processors.get(method)
        return processor_class() if processor_class else None

    # ---------------- HISTORY ---------------- #

    def getTransactionHistory(self):
        return self.transactionHistory