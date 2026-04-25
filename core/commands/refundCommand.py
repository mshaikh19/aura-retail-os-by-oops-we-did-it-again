from .command import Command


class RefundCommand(Command):
    # concrete command for handling refund operation

    def __init__(self, paymentMethod):
        self.paymentMethod = paymentMethod

    def execute(self, core):
        print("[Refund] Processing refund for last transaction")

        # ensure payment system is available
        if core.paymentSystem is None:
            raise Exception("Payment system unavailable")

        # process refund via PaymentSystem (uses Adapter Pattern)
        success = core.paymentSystem.refund(self.paymentMethod)

        if not success:
            raise Exception("Refund failed")
        
        print("[Refund] Refund completed successfully.")

        self.log()  # log execution