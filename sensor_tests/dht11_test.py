import time
import board
import adafruit_dht

def test_dht11():
    print("Initializing DHT11 test...")
    print("WARNING: Make sure you have installed 'adafruit-circuitpython-dht' via pip:")
    print("pip3 install adafruit-circuitpython-dht\n")

    # Define the GPIO Pin the data line is connected to (GPIO4 is standard)
    pin = board.D4

    try:
        # Create DHT11 object
        dht_device = adafruit_dht.DHT11(pin)
        print("DHT11 connected on GPIO 4!")
        print("Reading data. Note: DHT11 takes about 2 seconds between reads.")
        print("Press Ctrl+C to stop.\n")

        while True:
            try:
                # Read DHT values
                temperature_c = dht_device.temperature
                humidity = dht_device.humidity

                if temperature_c is not None and humidity is not None:
                    print(f"Temp: {temperature_c:.1f} °C   |   Humidity: {humidity:.1f}%")
                else:
                    print("Reading failed. Trying again...")

            except RuntimeError as error:
                # Runtime errors are very common with DHT11, just retry
                print(f"[Warn] DHT reading error: {error.args[0]}")
            
            # Wait 2.0 seconds between reads (DHT11 is slow)
            time.sleep(2.0)

    except KeyboardInterrupt:
        print("\nTest stopped by user.")
    except Exception as e:
        print(f"\n[ERROR] DHT11 execution failed: {e}")
        print("-> Make sure you are running with sufficient privileges if required.")
        print("-> Check wiring:")
        print("   VCC  -> 3.3V or 5V")
        print("   GND  -> GND")
        print("   DATA -> GPIO4 (Pin 7)")
    finally:
        try:
            dht_device.exit()
        except:
            pass

if __name__ == '__main__':
    test_dht11()
