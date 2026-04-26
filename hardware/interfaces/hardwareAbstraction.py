from hardware.interfaces.sensorMotorModule import SensorMotorModule
from utils.colors import Colors
import time

class HardwareAbstraction:
    """
    Bridge Pattern — Abstraction

    Controls hardware operations without depending on specific dispenser types.
    """

    def __init__(self, dispenser, sensorMotor=None):
        self._dispenser = dispenser
        self._sensorMotor = sensorMotor if sensorMotor else SensorMotorModule()

    def swapDispenser(self, newDispenser):
        """
        Replace current dispenser at runtime
        """
        self._dispenser = newDispenser
        print(f"{Colors.BLUE}[HW]{Colors.RESET} Dispenser swapped to {Colors.BOLD}{newDispenser.__class__.__name__}{Colors.RESET}")
        time.sleep(0.3)

    def dispenseProduct(self, product_name, quantity):
        """
        Main method used by system to dispense products
        """
        print(f"{Colors.BLUE}[HW]{Colors.RESET} Starting dispense process...")
        time.sleep(0.4)

        # start motor
        self._sensorMotor.startMotor()

        # call actual dispenser
        success = self._dispenser.dispense(product_name, quantity)

        # stop motor
        self._sensorMotor.stopMotor()

        if not success:
            print(f"{Colors.ERROR}[HW ERROR] Dispense failed{Colors.RESET}")
            return False

        print(f"{Colors.SUCCESS}[HW] Dispense successful{Colors.RESET}")
        time.sleep(0.3)
        return True

    def runCalibration(self):
        """
        Calibrate hardware
        """
        print("[HW] Running calibration...")
        return self._dispenser.calibrate()

    def getStatus(self):
        """
        Returns combined hardware status
        """
        return {
            "dispenser": self._dispenser.getStatus(),
            "motorRunning": self._sensorMotor.isMotorRunning()
        }