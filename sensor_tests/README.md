# CubeSat Hardware Test Scripts

This directory contains standalone Python test scripts to independently verify each hardware module of your CubeSat running on a Raspberry Pi 4 Model B.

## Setup & Dependencies

Before running the scripts, you must install the required dependencies and enable hardware interfaces.

### 1. Enable Hardware Interfaces
Open the Raspberry Pi configuration menu via SSH or Terminal:
```bash
sudo raspi-config
```
* Go to **Interfacing Options**
* Enable **I2C** (for MPU9250 and BMP180)
* Enable **SPI** (for LoRa RA-02)
* Reboot the Raspberry Pi.

### 2. Install System Packages
```bash
sudo apt update
sudo apt install -y python3-pip python3-smbus i2c-tools libgpiod2
```

### 3. Install Python Libraries
Install the specialized hardware interaction libraries via `pip`:

```bash
# Core wiring dependencies
pip3 install RPi.GPIO adafruit-blinka smbus2

# Library for MPU9250 (IMU)
pip3 install mpu9250-jmdev

# Library for DHT11
pip3 install adafruit-circuitpython-dht

# Library for LoRa RA-02 (SX1278)
pip3 install adafruit-circuitpython-rfm9x
```

---

## Test Scripts Overview

### 1. MPU9250 (IMU - Accelerometer, Gyroscope, Magnetometer)
The MPU9250 communicates over **I2C**.
* **VCC:** 3.3V
* **GND:** GND
* **SDA:** GPIO 2 (Pin 3)
* **SCL:** GPIO 3 (Pin 5)

**Run the test:**
```bash
python3 mpu9250_test.py
```

### 2. BMP180 (Barometer & Temperature)
The BMP180 communicates over **I2C**. This script uses native `smbus` so no external third-party PIP library specifically for the sensor is needed.
* **VCC:** 3.3V
* **GND:** GND
* **SDA:** GPIO 2 (Pin 3)
* **SCL:** GPIO 3 (Pin 5)

**Run the test:**
```bash
python3 bmp180_test.py
```

### 3. LoRa RA-02 (SX1278 Radio)
The LoRa module uses hardware **SPI**.
* **VCC:** 3.3V
* **GND:** GND
* **SCK:** GPIO 11 (Pin 23)
* **MOSI:** GPIO 10 (Pin 19)
* **MISO:** GPIO 9 (Pin 21)
* **NSS / CS:** GPIO 5 (Pin 29)
* **RST / Reset:** GPIO 6 (Pin 31)

**Run the test:**
```bash
python3 lora_test.py
```

### 4. DHT11 (Humidity & Temperature)
The DHT11 uses a single digital **GPIO** pin.
* **VCC:** 3.3V or 5V
* **GND:** GND
* **DATA:** GPIO 4 (Pin 7)

**Run the test:**
```bash
python3 dht11_test.py
```

---
*Note: You can verify your I2C connections (MPU9250 and BMP180) are visible to the Raspberry Pi by running `i2cdetect -y 1` in the terminal. The BMP180 should show up at address `77` and the MPU9250 should show up at address `68`.*
