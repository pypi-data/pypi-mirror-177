#ifndef _COMMON_HPP_
#define _COMMON_HPP_


#include "mraa/common.hpp"
#include "mraa/i2c.hpp"
#include <iostream>
#include <unistd.h>
#include <assert.h>
#include <algorithm>
#include <cstdlib>
#include <cstdio>
#include <cstdint>
#include <string>
#include <vector>
#include <map>
#include <thread>

uint8_t sensorId = 0;

class SensorBatch;

class Sensor {
    protected:
        uint8_t _sensorId;
        uint8_t _i2cBus;
        uint8_t _i2cAddress;
        friend SensorBatch;
    public:
        std::string sensorName;
        Sensor(uint8_t i2cBus, uint8_t i2cAddress)
        : _i2cBus(i2cBus), _i2cAddress(i2cAddress)
        {
            sensorName = "Sensor" + std::to_string(sensorId);
            _sensorId = sensorId;
            sensorId++;
        }
        virtual void sync_read_data(mraa::I2c& i2cBus, uint8_t* data) {

        }
        virtual void async_read_data(mraa::I2c& i2cBus) {

        }
        virtual void await_read_data(mraa::I2c& i2cBus, uint8_t* data) {

        }
        virtual void init(mraa::I2c& i2cBus, uint8_t* data) {

        }
        virtual void configure(mraa::I2c& i2cBus, uint8_t* data) {

        }
        virtual void close(mraa::I2c& i2cBus, uint8_t* data) {

        }
        virtual uint8_t get_sensor_id(void) const {
            return  _sensorId;
        }
        virtual uint8_t get_i2c_address(void) const {
            return _i2cAddress;
        }
        virtual uint8_t get_i2c_bus(void) const {
            return _i2cBus;
        }

};

void reading_thread() {

}

class SensorBatch {
    protected:
        std::map<uint8_t, mraa::I2c> _i2cBusMap;
        std::map<uint8_t, std::vector<Sensor*>> _sensorPtrMap;
    public:
        SensorBatch() {

        }
        template <typename T>
        bool add_sensor(T& sensor) {
            auto busIndexFound = _sensorPtrMap.find(sensor._i2cBus);
            if (busIndexFound == _sensorPtrMap.end()) {
                _sensorPtrMap.insert(std::pair<uint8_t, std::vector<Sensor*>>(sensor._i2cBus, std::vector<Sensor*>()));
            } else {
                int sensorArraySize = busIndexFound->second.size();
                for (int i = 0; i < sensorArraySize; i++) {
                    if (_sensorPtrMap[sensor._i2cBus][i]->_i2cAddress == sensor._i2cAddress) {
                        fprintf(stderr, "Warning: I2C Address Conflict on `i2c-%hhu` Detected! Sensor: `%s` will NOT be added!\n", sensor._i2cBus, sensor.sensorName.c_str());
                        return false;
                    }
                }
            }
            _sensorPtrMap[sensor._i2cBus].push_back(&sensor);
            return true;
        }
        bool start_reading() {
            fprintf(stderr, "Unimplemented Method\n");
            return false;
        }
        bool stop_reading() {
            fprintf(stderr, "Unimplemented Method\n");
            return false;
        }
};

#endif