# Enhanced-ICM20948 Python Library

## 1. Introduction

Based on [libmraa](https://github.com/eclipse/mraa), this library aims to provide a tool for generic Linux boards to read data from [ICM-20948 9-Axis MotionTracking device](https://invensense.tdk.com/products/motion-tracking/9-axis/icm-20948/) at a high speed(200Hz+ for accelerometer,gyroscope and 100Hz for magnetometer).

The core of the library is written in C++, with the help of [Pybind11](https://github.com/pybind/pybind11.git) providing Python bindings. The library also supports reading data from multiple ICM-20948 simultaneously from multiple I2C Bus(Works with single I2C Bus as long as there is no address conflict. However, limited by I2C Bus Frequency, the speed of reading data may be restricted)

The library is a part of two students’ Undergraduate Final Year Project conducted in NUS(Suzhou) Research Institute, Zhejiang University and University of Electronic Science and Technology of China.

At present, the library is under development.

If you have problems with the library or find any bugs during usage, feel free to contact with us: flyinghorse0510@zju.edu.cn or 2019021412017@std.uestc.edu.cn



## 2. Installation

### 2.1 Install Dependencies

For Ubuntu-based systems, you can install dependencies by the following commands:

```bash
sudo apt update
sudo apt install git build-essential swig3.0 libnode-dev cmake libjson-c-dev python3-pip python3-dev
```

### 2.2 Install libmraa

If your currently used boards have official supports for [libmraa](https://github.com/eclipse/mraa), it will be highly recommended that you install libmraa through the corresponding package manager or under tutorials provided by boards’ manufacturers. 

If not, following instructions may help you to some extent:

#### 2.2.1 Get Source Code

```bash
git clone https://github.com/eclipse/mraa.git
```

#### 2.2.2 Compile libmraa

```bash
cd mraa
mkdir build
cd build
#########################################
###### if you use ARM-based boards ######
cmake .. -DBUILDSWIGPYTHON=OFF -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILDARCH=arm
###### if you use X86-based boards ######
cmake .. -DBUILDSWIGPYTHON=OFF -DCMAKE_INSTALL_PREFIX:PATH=/usr
#########################################
make -j
```

#### 2.2.3 Install Compiled Files

```bash
sudo make install
sudo ldconfig
```

### 2.3 Install Enhanced-ICM20948

```
python3 -m pip install enhanced-icm20948==0.0.6
```

## 3. Usage Examples



