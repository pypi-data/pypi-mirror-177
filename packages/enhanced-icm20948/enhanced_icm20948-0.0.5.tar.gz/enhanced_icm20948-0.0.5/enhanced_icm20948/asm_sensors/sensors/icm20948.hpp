#ifndef _ICM20948_HPP_
#define _ICM20948_HPP_
#include "../common.hpp"
namespace ICM20948 {

    uint8_t ICM20948_DEFAULT_I2C_ADDRESS =          (uint8_t)(0x69);
    uint8_t ICM20948_ALT_I2C_ADDRESS =              (uint8_t)(0x68);

    uint8_t CORRECT_WHO_AM_I_VALUE =                (uint8_t)(0xEA);
    uint8_t BANK_SEL_REG_ADDR =                     (uint8_t)(0x7F);

    // Bank 0 Register
    uint8_t WHO_AM_I_REG_ADDR =                     (uint8_t)(0x00);
    uint8_t USER_CTRL_REG_ADDR =                    (uint8_t)(0x03);
    uint8_t LP_CONFIG_REG_ADDR =                    (uint8_t)(0x05);
    uint8_t POWER_MANAGEMENT_REG_1_ADDR =           (uint8_t)(0x06);
    uint8_t POWER_MANAGEMENT_REG_2_ADDR =           (uint8_t)(0x07);
    uint8_t INT_PIN_CFG_REG_ADDR =                  (uint8_t)(0x0F);
    uint8_t ACCEL_XOUT_H_REG_ADDR =                 (uint8_t)(0x2D); // first byte of accelerometeR = data address
    uint8_t GYRO_XOUT_H_REG_ADDR =                  (uint8_t)(0x33); // first byte of gyroscope data address
    uint8_t I2C_MST_STATUS_REG_ADDR =               (uint8_t)(0x17);
    uint8_t EXT_SLV_SENS_DATA_00_REG_ADDR =         (uint8_t)(0x3B);

    // Bank 1 Register


    // Bank 2 Register
    uint8_t GYRO_SMPLRT_DIV_REG_ADDR =              (uint8_t)(0x00);
    uint8_t GYRO_CONFIG_1_REG_ADDR =                (uint8_t)(0x01);
    uint8_t GYRO_CONFIG_2_REG_ADDR =                (uint8_t)(0x02);
    uint8_t ACCEL_SMPLRT_DIV_1_REG_ADDR =           (uint8_t)(0x10);
    uint8_t ACCEL_SMPLRT_DIV_2_REG_ADDR =           (uint8_t)(0x11);
    uint8_t ACCEL_CONFIG_1_REG_ADDR =               (uint8_t)(0x14);
    uint8_t ACCEL_CONFIG_2_REG_ADDR =               (uint8_t)(0x15);

    // Bank 3 Register
    uint8_t I2C_MST_ODR_CONFIG_REG_ADDR =           (uint8_t)(0x00);
    uint8_t I2C_MST_CTRL_REG_ADDR =                 (uint8_t)(0x01);
    uint8_t I2C_MST_DELAY_CTRL_REG_ADDR =           (uint8_t)(0x02);
    uint8_t I2C_SLV0_ADDR_REG_ADDR =                (uint8_t)(0x03);
    uint8_t I2C_SLV0_REG_REG_ADDR =                 (uint8_t)(0x04);
    uint8_t I2C_SLV0_CTRL_REG_ADDR =                (uint8_t)(0x05);
    uint8_t I2C_SLV0_DO_REG_ADDR =                  (uint8_t)(0x06);
    uint8_t I2C_SLV4_ADDR_REG_ADDR =                (uint8_t)(0x13);
    uint8_t I2C_SLV4_REG_REG_ADDR =                 (uint8_t)(0x14);
    uint8_t I2C_SLV4_CTRL_REG_ADDR =                (uint8_t)(0x15);
    uint8_t I2C_SLV4_DO_REG_ADDR =                  (uint8_t)(0x16);
    uint8_t I2C_SLV4_DI_REG_ADDR =                  (uint8_t)(0x17);

    class ICM20948: public Sensor {
        protected:
            friend SensorBatch;
        public:
            ICM20948(uint8_t i2cBusIndex, uint8_t i2cAddress = ICM20948_DEFAULT_I2C_ADDRESS)
            : Sensor(i2cBusIndex, i2cAddress)
            {}
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
    };
}
#endif