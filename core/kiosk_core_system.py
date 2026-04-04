class KioskCoreSystem:
    def __init__(self, inventory_system=None, payment_system=None, hardware_system=None):
        """
        Initialize the core system with subsystem references
        """
        self.inventory_system = inventory_system
        self.payment_system = payment_system
        self.hardware_system = hardware_system

        # System states
        self.system_status = "ACTIVE"   # ACTIVE, ERROR, EMERGENCY

    def execute_command(self, command):
        """
        Executes a given command after checking system status
        """
        if not self.check_system_status():
            print("System is not operational. Cannot execute command.")
            return

        try:
            print(f"Executing command: {command.__class__.__name__}")
            command.execute()
            print("Command executed successfully.")

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            self.system_status = "ERROR"

    def check_system_status(self):
        """
        Checks if the system is in a valid state to execute operations
        """
        if self.system_status == "ERROR":
            print("System is in ERROR state.")
            return False

        if self.system_status == "EMERGENCY":
            print("System is in EMERGENCY mode. Limited operations allowed.")
            return True

        return True

    def set_system_status(self, status):
        """
        Update system status
        """
        valid_states = ["ACTIVE", "ERROR", "EMERGENCY"]
        if status in valid_states:
            self.system_status = status
        else:
            print("Invalid system status.")

    def get_system_status(self):
        """
        Returns current system status
        """
        return self.system_status
