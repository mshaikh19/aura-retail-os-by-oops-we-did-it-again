from hardware.interfaces.sensorMotorModule import SensorMotorModule


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
        print(f"[HW] Dispenser swapped to {newDispenser.__class__.__name__}")

    def dispenseProduct(self, product_name, quantity):
        """
        Main method used by system to dispense products
        """
        print("[HW] Starting dispense process...")

        # start motor
        self._sensorMotor.startMotor()

        # call actual dispenser
        success = self._dispenser.dispense(product_name, quantity)

        # stop motor
        self._sensorMotor.stopMotor()

        if not success:
            print("[HW ERROR] Dispense failed")
            return False

        print("[HW] Dispense successful")
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