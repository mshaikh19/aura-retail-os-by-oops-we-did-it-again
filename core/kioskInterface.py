class KioskInterface:
    def __init__(self, coreSystem):
        self.core = coreSystem

    def purchaseItem(self, productId, quantity):
        if not productId or quantity <= 0:
            print("Invalid input for purchase")
            return
        
        print(f"Request: Purchase {quantity} of {productId}")
        self.core.handleRequest("purchase", productId, quantity)

    def refundTransaction(self, transactionId):
        if not transactionId:
            print("Invalid transaction ID")
            return
        
        print(f"Request: Refund transaction {transactionId}")
        self.core.handle_request("refund", transactionId)

    def restockInventory(self, productId, quantity):
        if not productId or quantity <= 0:
            print("Invalid input for restock")
            return
        
        print(f"Request: Restock {quantity} of {productId}")
        self.core.handleRequest("restock", productId, quantity)

    def runDiagnostics(self):
        print("Request: Running diagnostics...")
        self.core.handleRequest("diagnostics")