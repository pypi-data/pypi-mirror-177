from enhanced_icm20948 import asm_sensors

__version__ = "0.0.6"
class Sensor:
    def __init__(self, core):
        self.core = core
        
    def get_name(self):
        return self.core.sensorName
    
    def set_name(self, name: str):
        self.core.sensorName = name
    
    def get_i2c_bus(self):
        return self.core.get_i2c_bus()
    
    def get_i2c_address(self):
        return self.core.get_i2c_address()
    
    def get_sensor_id(self):
        return self.core.get_sensor_id()
    

class ICM20948(Sensor):
    def __init__(self, i2cBus: int, i2cAddress: int = asm_sensors.ICM20948_DEFAULT_I2C_ADDRESS, sensorName: str = ""):
        super().__init__(asm_sensors.ICM20948(i2cBus, i2cAddress))
        if (len(sensorName) > 0):
            self.set_name(sensorName)

        
        
class SensorBatch:
    def __init__(self):
        self.core = asm_sensors.SensorBatch()
    
    def add_sensor(self, sensor):
        return self.core.add_sensor(sensor.core)
    
    def start_reading(self):
        return self.core.start_reading()
        
    def stop_reading(self):
        return self.core.stop_reading()
        