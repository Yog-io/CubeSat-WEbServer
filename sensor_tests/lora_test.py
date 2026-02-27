import time
import busio
import digitalio
import board
import adafruit_rfm9x

# RA-02 uses the SX1278 chip, usually running at 433 MHz
RADIO_FREQ_MHZ = 433.0

def test_lora():
    print("Initializing LoRa RA-02 (SX1278) test...")
    print("WARNING: Make sure you have installed 'adafruit-circuitpython-rfm9x' via pip:")
    print("pip3 install adafruit-circuitpython-rfm9x\n")

    try:
        # Define SPI pins mapped to Raspberry Pi hardware SPI
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # Define Chip Select (CS) and Reset pins
        # Adjust these if your wiring is different
        cs = digitalio.DigitalInOut(board.D5)
        reset = digitalio.DigitalInOut(board.D6)

        # Initialize the LoRa module
        rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, RADIO_FREQ_MHZ)
        
        # Optional: Set transmit power. Max is 23 (keep it low for testing)
        rfm9x.tx_power = 23

        print(f"LoRa module initialized successfully on {RADIO_FREQ_MHZ} MHz!")
        
        # Transmit a test message
        print("\nSending a test message: 'Ping from Pi CubeSat'")
        rfm9x.send(bytes("Ping from Pi CubeSat", "utf-8"))
        print("Message sent successfully!")

        print("\nGoing into listening mode... waiting to receive packets.")
        print("Press Ctrl+C to stop.")

        while True:
            # Wait for a packet
            packet = rfm9x.receive(timeout=1.0)
            
            if packet is None:
                # No packet received
                continue

            print("\n<<< Packet Received! >>>")
            print(f"Raw Bytes: {packet}")
            
            # Attempt to decode as ASCII/UTF-8
            try:
                packet_text = str(packet, 'utf-8')
                print(f"Text Decoded: {packet_text}")
            except UnicodeDecodeError:
                print("Text Decoded: [Non-ASCII data]")
                
            # Print Signal Strength
            print(f"Signal Strength (RSSI): {rfm9x.last_rssi} dB")

    except KeyboardInterrupt:
        print("\nTest stopped by user.")
    except Exception as e:
        print(f"\n[ERROR] LoRa Initialization/Testing failed: {e}")
        print("-> Ensure SPI is enabled on your Raspberry Pi (sudo raspi-config > Interfaces > SPI).")
        print("-> Check your wiring:")
        print("   VCC  -> 3.3V")
        print("   GND  -> GND")
        print("   SCK  -> GPIO11 (Pin 23)")
        print("   MOSI -> GPIO10 (Pin 19)")
        print("   MISO -> GPIO9  (Pin 21)")
        print("   NSS  -> GPIO5  (Pin 29)")
        print("   RST  -> GPIO6  (Pin 31)")
        print("-> Also ensure 'adafruit-blinka' and 'rpi.gpio' are installed.")

if __name__ == '__main__':
    test_lora()
