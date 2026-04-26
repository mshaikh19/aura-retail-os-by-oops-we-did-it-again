from utils.colors import Colors
import time

class SensorMotorModule:
    """
    Simulates motor and sensor layer of hardware system
    """

    def __init__(self):
        self._motorRunning = False
        self._sensorReadings = {}

    def startMotor(self):
        self._motorRunning = True
        print(f"{Colors.SUCCESS}[MOTOR]{Colors.RESET} Motor started")
        time.sleep(0.2)

    def stopMotor(self):
        self._motorRunning = False
        print(f"{Colors.SUCCESS}[MOTOR]{Colors.RESET} Motor stopped")
        time.sleep(0.2)

    def isMotorRunning(self):
        return self._motorRunning

    def readSensor(self, sensor_id):
        return self._sensorReadings.get(sensor_id, None)

    def updateSensor(self, sensor_id, value):
        self._sensorReadings[sensor_id] = value
        print(f"[SENSOR] {sensor_id} updated to {value}")