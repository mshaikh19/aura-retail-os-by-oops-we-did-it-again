from .command import Command


class RefundCommand(Command):
    def __init__(self, amount, paymentMethod):
        self.amount = amount
        self.paymentMethod = paymentMethod

    def execute(self, core):
        print(f"[Refund] Processing refund of ₹{self.amount}")

        # 1. Validate input
        if self.amount <= 0:
            raise Exception("Invalid refund amount")

        # 2. Check payment system
        if core.paymentSystem is None:
            raise Exception("Payment system unavailable")

        # 3. Process refund
        core.paymentSystem.refund(self.paymentMethod, self.amount)

        print("[Refund] Refund completed successfully.")
        self.log()