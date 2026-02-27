import smbus
import time

I2C_BUS = 1
BMP180_ADDRESS = 0x77  # Default I2C address for BMP180

# BMP180 Registers
CALIB_START = 0xAA
CONTROL = 0xF4
DATA = 0xF6
COMMAND_TEMP = 0x2E

def convert_to_signed_16(msb, lsb):
    val = (msb << 8) | lsb
    if val > 32767:
        val -= 65536
    return val

def test_bmp180():
    print("Initializing BMP180 (Barometer) test...")
    try:
        bus = smbus.SMBus(I2C_BUS)
        
        # 1. Verify Device ID
        chip_id = bus.read_byte_data(BMP180_ADDRESS, 0xD0)
        if chip_id != 0x55:
            print(f"[ERROR] Found I2C device, but Chip ID mismatch! (Expected 0x55, got {hex(chip_id)})")
            return
            
        print("BMP180 successfully detected on I2C bus (ID: 0x55).")
        
        # 2. Read calibration data for Temperature
        # We read a few bytes to ensure we can communicate properly
        calib_data = bus.read_i2c_block_data(BMP180_ADDRESS, CALIB_START, 22)
        AC5 = (calib_data[8] << 8) | calib_data[9]
        AC6 = (calib_data[10] << 8) | calib_data[11]
        MC = convert_to_signed_16(calib_data[18], calib_data[19])
        MD = convert_to_signed_16(calib_data[20], calib_data[21])
        
        print("Calibration data read successfully. Starting temperature readings...")
        print("(Press Ctrl+C to stop)\n")
        
        while True:
            # Request Temperature Reading
            bus.write_byte_data(BMP180_ADDRESS, CONTROL, COMMAND_TEMP)
            time.sleep(0.005)  # Wait 5ms (max required time is 4.5ms)
            
            # Read Raw Temperature
            msb = bus.read_byte_data(BMP180_ADDRESS, DATA)
            lsb = bus.read_byte_data(BMP180_ADDRESS, DATA+1)
            UT = (msb << 8) | lsb
            
            # Calculate True Temperature
            X1 = ((UT - AC6) * AC5) >> 15
            X2 = (MC << 11) // (X1 + MD)
            B5 = X1 + X2
            temp = ((B5 + 8) >> 4) / 10.0
            
            print(f"Current Temperature: {temp:.2f} °C")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nTest stopped by user.")
    except Exception as e:
        print(f"\n[ERROR] Communication failed: {e}")
        print("-> Ensure I2C is enabled on your Raspberry Pi.")
        print("-> Check wiring: VCC to 3.3V, GND to GND, SDA to GPIO2, SCL to GPIO3.")
        print("-> Run 'i2cdetect -y 1' to verify device is detected at 0x77.")

if __name__ == '__main__':
    test_bmp180()
