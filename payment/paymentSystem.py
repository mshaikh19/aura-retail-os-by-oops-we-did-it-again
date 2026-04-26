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
        
        # Convert raw dictionaries back to Transaction objects
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

        # Process payment using adapter
        result = processor.processPayment(amount)

        if result:
            transaction = Transaction(
                product_name=product_name if product_name else "UNKNOWN",
                quantity=quantity if quantity else 0,
                total_amount=amount,
                payment_method=method,
                status="SUCCESS",
                kiosk_type=kiosk_type
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

        print(f"{Colors.WARNING}[PAYMENT]{Colors.RESET} Payment completed")
        return None

    # ---------------- REFUND ---------------- #

    def refund(self, method):
        print(f"\n{Colors.WARNING}[PAYMENT]{Colors.RESET} Starting refund...")

        # Get the current session to filter refunds
        active_session = SessionManager().getActiveSession()
        if not active_session:
            print(f"{Colors.ERROR}[PAYMENT ERROR]{Colors.RESET} No active session found. Cannot process refund.")
            return False

        # Find the last transaction that belongs to THIS session
        session_tx_ids = active_session.transaction_ids
        session_transactions = [t for t in self.transactionHistory if t.transaction_id in session_tx_ids]

        if not session_transactions:
            print(f"{Colors.WARNING}[PAYMENT]{Colors.RESET} No transactions found in the current session.")
            return False

        # Get the last transaction from THIS session
        last_transaction = session_transactions[-1]

        # Prevent double refund
        if last_transaction.status == "REFUNDED":
            print(f"{Colors.WARNING}[PAYMENT]{Colors.RESET} Last transaction already refunded")
            return False

        processor = self._getProcessor(method)

        if processor is None:
            print(f"{Colors.ERROR}[PAYMENT ERROR]{Colors.RESET} Invalid payment method")
            return False

        amount = last_transaction.total_amount

        print(f"{Colors.WARNING}[PAYMENT]{Colors.RESET} Refunding Rs.{amount} for {last_transaction.product_name}")

        result = processor.refundPayment(amount)

        if result:
            # Update transaction status
            last_transaction.status = "REFUNDED"

            # Save updated transaction
            PersistentLayer.saveTransaction(last_transaction.toDict())

            # Notify monitoring system
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