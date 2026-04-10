from .command import Command


class RefundCommand(Command):
    # concrete command for handling refund operation

    def __init__(self, amount, paymentMethod):
        self.amount = amount
        self.paymentMethod = paymentMethod

    def execute(self, core):
        print(f"[Refund] Processing refund of ₹{self.amount}")

        # validate refund amount
        if self.amount <= 0:
            raise Exception("Invalid refund amount")

        # ensure payment system is available
        if core.paymentSystem is None:
            raise Exception("Payment system unavailable")

        # process refund via PaymentSystem (uses Adapter Pattern)
        core.paymentSystem.refund(self.paymentMethod, self.amount)

        print("[Refund] Refund completed successfully.")

        self.log()  # log execution