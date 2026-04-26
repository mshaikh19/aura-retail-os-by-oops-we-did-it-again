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
        print("\n[PaymentSystem] Starting payment...")   

        processor = self._getProcessor(method)

        if processor is None:
            print("[PaymentSystem] Invalid payment method")
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

            print("[PaymentSystem] Transaction recorded successfully.")

        else:
            transaction = Transaction(
                product_name=product_name if product_name else "UNKNOWN",
                quantity=quantity if quantity else 0,
                total_amount=amount,
                payment_method=method,
                status="FAILED",
                kiosk_type=kiosk_type
            )   

            self.transactionHistory.append(transaction)
            PersistentLayer.saveTransaction(transaction.toDict())

            MonitoringSystem.notify(
                "PAYMENT",
                "TRANSACTION_FAILED",
                f"Rs.{amount} via {method}"
            )

        if result:
            print("[PaymentSystem] Payment completed successfully")
        else:
            print("[PaymentSystem] Payment failed")
        return result

    # ---------------- REFUND ---------------- #

    def refund(self, method):
        print("\n[PaymentSystem] Starting refund...")

        # No transactions
        if not self.transactionHistory:
            print("[PaymentSystem] No transactions available for refund")
            return False

        # Get last transaction
        last_transaction = self.transactionHistory[-1]

        # Prevent double refund
        if last_transaction.status == "REFUNDED":
            print("[PaymentSystem] Last transaction already refunded")
            return False

        processor = self._getProcessor(method)

        if processor is None:
            print("[PaymentSystem] Invalid payment method")
            return False

        amount = last_transaction.total_amount

        print(f"[PaymentSystem] Refunding Rs.{amount} for {last_transaction.product_name}")

        result = processor.refundPayment(amount)

        if result:
            # Update transaction status
            last_transaction.status = "REFUNDED"

            refund_txn = Transaction(
                product_name=last_transaction.product_name,
                quantity=last_transaction.quantity,
                total_amount=amount,
                payment_method=method,
                status="REFUNDED",
                kiosk_type=last_transaction.kiosk_type
            )

            self.transactionHistory.append(refund_txn)
            # Save updated transaction
            PersistentLayer.saveTransaction(refund_txn.toDict())

            # Notify monitoring system
            MonitoringSystem.notify(
                "PAYMENT",
                "REFUND_COMPLETE",
                f"Rs.{amount} refunded via {method}"
            )

            print("[PaymentSystem] Refund successful")

        print("[PaymentSystem] Refund completed")
        return result


    # ---------------- ROLLBACK ---------------- #

    def rollbackLastPayment(self, method):
        """
        Atomic rollback support (for hardware failure case)
        """
        print("\n[PaymentSystem] Rolling back last payment...")

        if not self.transactionHistory:
            print("[PaymentSystem] No transaction to rollback")
            return False

        last_transaction = self.transactionHistory[-1]

        if last_transaction.status != "SUCCESS":
            print("[PaymentSystem] Cannot rollback non-success transaction")
            return False

        amount = last_transaction.total_amount

        processor = self._getProcessor(method)

        if processor is None:
            print("[PaymentSystem] Invalid payment method")
            return False

        result = processor.refundPayment(amount)

        if result:
            last_transaction.status = "ROLLED_BACK"

            rollback_txn = Transaction(
                product_name=last_transaction.product_name,
                quantity=last_transaction.quantity,
                total_amount=amount,
                payment_method=method,
                status="ROLLED_BACK",
                kiosk_type=last_transaction.kiosk_type
            )

            self.transactionHistory.append(rollback_txn)
            PersistentLayer.saveTransaction(rollback_txn.toDict())

            MonitoringSystem.notify(
                "PAYMENT",
                "ROLLBACK",
                f"Rs.{amount} rolled back via {method}"
            )

            print("[PaymentSystem] Rollback successful")

        else:
            print("[CRITICAL] Rollback failed!")

        return result    

    # ---------------- HELPER ---------------- #

    def _getProcessor(self, method):
        processor_class = self.processors.get(method)
        return processor_class() if processor_class else None

    # ---------------- HISTORY ---------------- #

    def getTransactionHistory(self):
        return self.transactionHistory