from hardware.interfaces.sensorMotorModule import SensorMotorModule
from utils.colors import Colors


class HardwareAbstraction:
    """
    Bridge Pattern — Abstraction

    Controls hardware operations without depending on specific dispenser types.
    """

    def __init__(self, dispenser, sensorMotor=None):
        self._dispenser = dispenser
        self._sensorMotor = sensorMotor if sensorMotor else SensorMotorModule()
        print(f" {Colors.CYAN}◈ {Colors.BOLD}HARDWARE:{Colors.RESET} {Colors.TEXT}Abstraction Layer bridged.{Colors.RESET}")

    def swapDispenser(self, newDispenser):
        """
        Replace current dispenser at runtime
        """
        self._dispenser = newDispenser
        print(f"{Colors.BLUE}[HW]{Colors.RESET} Dispenser swapped to {newDispenser.__class__.__name__}")

    def dispenseProduct(self, product_name, quantity):
        """
        Main method used by system to dispense products
        """
        print(f"{Colors.BLUE}[HW]{Colors.RESET} Starting dispense process...")

        # start motor
        self._sensorMotor.startMotor()

        # call actual dispenser
        success = self._dispenser.dispense(product_name, quantity)

        # stop motor
        self._sensorMotor.stopMotor()

        if not success:
            print(f"{Colors.ERROR}[HW ERROR]{Colors.RESET} Dispense failed")
            return False

        print(f"{Colors.BLUE}[HW]{Colors.RESET} Dispense successful")
        return True

    def runCalibration(self):
        """
        Calibrate hardware
        """
        print(f"{Colors.BLUE}[HW]{Colors.RESET} Running calibration...")
        return self._dispenser.calibrate()

    def getStatus(self):
        """
        Returns combined hardware status
        """
        return {
            "dispenser": self._dispenser.getStatus(),
            "motorRunning": self._sensorMotor.isMotorRunning()
        }