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
import time

class PaymentSystem:

    def __init__(self):
        # Store all transactions in memory
        self.transactionHistory = []

         # Factory mapping for payment processors
        self.processors = {
            "UPI": UPIAdapter,
            "CARD": CardAdapter,
            "WALLET": WalletAdapter
        }

    # ---------------- PAYMENT ---------------- #

    def makePayment(self, method, amount, product_name=None, quantity=None, kiosk_type="UNKNOWN"):
        print(f"\n{Colors.WARNING}[PaymentSystem]{Colors.RESET} Starting payment...")
        time.sleep(0.4)

        processor = self._getProcessor(method)

        if processor is None:
            print(f"{Colors.ERROR}[PaymentSystem] Invalid payment method{Colors.RESET}")
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

            print(f"{Colors.SUCCESS}[PaymentSystem] Transaction recorded successfully.{Colors.RESET}")
            time.sleep(0.3)

        print(f"{Colors.WARNING}[PaymentSystem]{Colors.RESET} Payment completed")
        time.sleep(0.3)
        return result

    # ---------------- REFUND ---------------- #

    def refund(self, method):
        print(f"\n{Colors.WARNING}[PaymentSystem]{Colors.RESET} Starting refund...")
        time.sleep(0.4)

        # No transactions
        if not self.transactionHistory:
            print(f"{Colors.ERROR}[PaymentSystem] No transactions available for refund{Colors.RESET}")
            return False

        # Get last transaction
        last_transaction = self.transactionHistory[-1]

        # Prevent double refund
        if last_transaction.status == "REFUNDED":
            print(f"{Colors.ERROR}[PaymentSystem] Last transaction already refunded{Colors.RESET}")
            return False

        processor = self._getProcessor(method)

        if processor is None:
            print(f"{Colors.ERROR}[PaymentSystem] Invalid payment method{Colors.RESET}")
            return False

        amount = last_transaction.total_amount

        print(f"{Colors.WARNING}[PaymentSystem]{Colors.RESET} Refunding {Colors.BOLD}Rs.{amount}{Colors.RESET} for {Colors.CYAN}{last_transaction.product_name}{Colors.RESET}")
        time.sleep(0.3)

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

            print(f"{Colors.SUCCESS}[PaymentSystem] Refund successful{Colors.RESET}")
            time.sleep(0.3)

        print(f"{Colors.WARNING}[PaymentSystem]{Colors.RESET} Refund completed")
        time.sleep(0.3)
        return result

    # ---------------- HELPER ---------------- #

    def _getProcessor(self, method):
        processor_class = self.processors.get(method)
        return processor_class() if processor_class else None

    # ---------------- HISTORY ---------------- #

    def getTransactionHistory(self):
        return self.transactionHistory