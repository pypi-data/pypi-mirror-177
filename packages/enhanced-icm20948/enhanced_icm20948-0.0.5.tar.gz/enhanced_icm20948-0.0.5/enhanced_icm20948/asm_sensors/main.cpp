#include <pybind11/pybind11.h>
#include "common.hpp"
#include "sensors.hpp"
namespace py = pybind11;


PYBIND11_MODULE(asm_sensors, m) {
    m.doc() = "An ultra-fast and powerful ICM20948 sensor reading library"; // optional module docstring

    py::class_<Sensor>(m, "Sensor")
        .def(py::init<uint8_t, uint8_t>(), py::arg("i2cBus"), py::arg("i2cAddress"))
        .def("get_sensor_id", &Sensor::get_sensor_id)
        .def("get_i2c_address", &Sensor::get_i2c_address)
        .def("get_i2c_bus", &Sensor::get_i2c_bus)
        .def_readwrite("sensorName", &Sensor::sensorName);
        
    py::class_<ICM20948::ICM20948, Sensor>(m, "ICM20948")
        .def(py::init<uint8_t, uint8_t>(), py::arg("i2cBus"), py::arg("i2cAddress") = ICM20948::ICM20948_DEFAULT_I2C_ADDRESS);

    py::class_<SensorBatch>(m, "SensorBatch")
        .def(py::init())
        .def("add_sensor", &SensorBatch::add_sensor<ICM20948::ICM20948>)
        .def("start_reading", &SensorBatch::start_reading)
        .def("stop_reading", &SensorBatch::stop_reading);

    m.attr("ICM20948_DEFAULT_I2C_ADDRESS") = ICM20948::ICM20948_DEFAULT_I2C_ADDRESS;
}