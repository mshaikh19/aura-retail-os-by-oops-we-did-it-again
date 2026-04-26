class SensorMotorModule:
    """
    Simulates motor and sensor layer of hardware system
    """

    def __init__(self):
        self._motorRunning = False
        self._sensorReadings = {}

    def startMotor(self):
        self._motorRunning = True
        print("[MOTOR] Motor started")

    def stopMotor(self):
        self._motorRunning = False
        print("[MOTOR] Motor stopped")

    def isMotorRunning(self):
        return self._motorRunning

    def readSensor(self, sensor_id):
        return self._sensorReadings.get(sensor_id, None)

    def updateSensor(self, sensor_id, value):
        self._sensorReadings[sensor_id] = value
        print(f"[SENSOR] {sensor_id} updated to {value}")