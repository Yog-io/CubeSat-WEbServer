import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

def test_mpu9250():
    print("Initializing MPU9250 (IMU) test...")
    print("WARNING: Make sure you have installed 'mpu9250-jmdev' via pip:")
    print("pip3 install mpu9250-jmdev\n")
    
    try:
        # Create an MPU9250 instance
        mpu = MPU9250(
            address_ak=AK8963_ADDRESS, 
            address_mpu_master=MPU9050_ADDRESS_68, # I2C Address 0x68
            address_mpu_slave=None, 
            bus=1,
            gfs=GFS_1000, 
            afs=AFS_8G, 
            mfs=AK8963_BIT_16, 
            mode=AK8963_MODE_C100HZ
        )
        
        # Configure and calibrate the sensor
        mpu.configure()
        print("MPU9250 configured successfully!")
        print("Waiting 1 second before reading...\n")
        time.sleep(1)
        
        print("Starting continuous data read (Press Ctrl+C to stop)...")
        while True:
            # Read sensor data
            accel = mpu.readAccelerometerMaster()
            gyro = mpu.readGyroscopeMaster()
            mag = mpu.readMagnetometerMaster()
            temp = mpu.readTemperatureMaster()
            
            # Print data
            print(f"Accel(g)   : X:{accel[0]:.2f}, Y:{accel[1]:.2f}, Z:{accel[2]:.2f}")
            print(f"Gyro(dps)  : X:{gyro[0]:.2f}, Y:{gyro[1]:.2f}, Z:{gyro[2]:.2f}")
            print(f"Mag(uT)    : X:{mag[0]:.2f}, Y:{mag[1]:.2f}, Z:{mag[2]:.2f}")
            print(f"Temp(C)    : {temp:.2f} °C")
            print("-" * 50)
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nTest stopped by user.")
    except Exception as e:
        print(f"\n[ERROR] Failed to run MPU9250: {e}")
        print("-> Ensure I2C is enabled on your Raspberry Pi (sudo raspi-config > Interfaces > I2C).")
        print("-> Check wiring: VCC to 3.3V, GND to GND, SDA to GPIO2, SCL to GPIO3.")
        print("-> Run 'i2cdetect -y 1' to verify device is detected at 0x68.")

if __name__ == '__main__':
    test_mpu9250()
