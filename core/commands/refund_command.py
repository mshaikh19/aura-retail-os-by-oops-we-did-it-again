from .command import Command


class RefundCommand(Command):
    def __init__(self, transactionId):
        self.transactionId = transactionId

    def execute(self, core):
        print(f"[Refund] Processing refund for transaction {self.transactionId}")

        if core.paymentSystem:
            print("[Refund] Reversing payment...")

        print("[Refund] Refund completed successfully.")

        self.log()