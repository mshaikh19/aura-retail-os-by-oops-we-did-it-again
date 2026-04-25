# Import adapter classes for different payment methods
from payment.adapters.upiAdapter import UPIAdapter
from payment.adapters.cardAdapter import CardAdapter
from payment.adapters.walletAdapter import WalletAdapter

# Import Transaction model
from models.transaction import Transaction

# Import Persistent Layer (your file name)
from persistence.persistenceLayer import PersistentLayer

# Import Monitoring System
from monitoring.monitoring_system import MonitoringSystem


class PaymentSystem:

    def __init__(self):
        # Store all transactions in memory
        self.transactionHistory = []

    def makePayment(self, method, amount, product_name=None, quantity=None, kiosk_type="UNKNOWN"):
        print("\n[PaymentSystem] Starting payment...")

        processor = self._getProcessor(method)

        if processor is None:
            print("[PaymentSystem] Invalid payment method")
            return False

        # Process payment using adapter
        result = processor.processPayment(amount)

        # ✅ After successful payment
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

            # ✅ Save to JSON (Persistence)
            PersistentLayer.saveTransaction(transaction.toDict())

            # ✅ Notify Monitoring System (Observer Pattern)
            MonitoringSystem.notify(
                "PAYMENT",
                "TRANSACTION_COMPLETE",
                f"Rs.{amount} via {method}"
            )

            print("[PaymentSystem] Transaction recorded successfully.")

        print("[PaymentSystem] Payment completed")
        return result

    def refund(self, method, amount):
        print("\n[PaymentSystem] Starting refund...")

        processor = self._getProcessor(method)

        if processor is None:
            print("[PaymentSystem] Invalid payment method")
            return False

        result = processor.refundPayment(amount)

        # (Optional: you can later log refund transactions)
        print("[PaymentSystem] Refund completed")
        return result

    def _getProcessor(self, method):
        if method == "UPI":
            return UPIAdapter()
        elif method == "CARD":
            return CardAdapter()
        elif method == "WALLET":
            return WalletAdapter()
        else:
            return None

    def getTransactionHistory(self):
        return self.transactionHistory