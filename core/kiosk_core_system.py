class KioskCoreSystem:
    def __init__(self, inventorySystem=None, paymentSystem=None, hardwareSystem=None):
       
        self.inventorySystem = inventorySystem
        self.paymentSystem = paymentSystem
        self.hardwareSystem = hardwareSystem

      
        self.systemStatus = "ACTIVE"  

        self.commandHistory = []

    def executeCommand(self, command):
        if not self.checkSystemStatus():
            print("System not ready. Cannot execute command.")
            return False

        try:
            print(f"\n[CORE] Executing {command.__class__.__name__}...")


            command.execute(self)


            self.commandHistory.append(command)

            print("[CORE] Command executed successfully.")
            return True

        except Exception as e:
            print(f"[CORE ERROR] {str(e)}")
            self.systemStatus = "ERROR"
            return False

    def checkSystemStatus(self):
      
        if self.systemStatus == "ERROR":
            print("[CORE] System in ERROR state.")
            return False

        if self.systemStatus == "EMERGENCY":
            print("[CORE] Emergency mode active. Limited operations.")
            return True

        return True

    def setSystemStatus(self, status):
        
        validStates = ["ACTIVE", "ERROR", "EMERGENCY"]

        if status in validStates:
            self.systemStatus = status
            print(f"[CORE] System status changed to {status}")
        else:
            print("[CORE] Invalid system status.")

    def getSystemStatus(self):
       
        return self.systemStatus

    def getCommandHistory(self):
      
        return self.commandHistory


# # Test block
# if __name__ == "__main__":
#     core = KioskCoreSystem()
#     print("System Status:", core.getSystemStatus())