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
        return result

    # ---------------- REFUND ---------------- #

    def refund(self, method):
        print(f"\n{Colors.WARNING}[PAYMENT]{Colors.RESET} Starting refund...")

        # No transactions
        if not self.transactionHistory:
            print(f"{Colors.WARNING}[PAYMENT]{Colors.RESET} No transactions available for refund")
            return False

        # Get last transaction
        last_transaction = self.transactionHistory[-1]

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