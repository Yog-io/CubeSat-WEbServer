import json
import time
import random
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "sensor_log.json")

def generate_mock_data():
    return {
        "timestamp": time.time(),
        "dht11": {
            "temperature": round(random.uniform(20.0, 35.0), 2),
            "humidity": round(random.uniform(40.0, 60.0), 2)
        },
        "bmp280": {
            "temperature": round(random.uniform(20.0, 35.0), 2),
            "pressure": round(random.uniform(950.0, 1050.0), 2),
            "altitude": round(random.uniform(100.0, 500.0), 2)
        },
        "mpu9250": {
            "accel": {
                "x": round(random.uniform(-1.0, 1.0), 3),
                "y": round(random.uniform(-1.0, 1.0), 3),
                "z": round(random.uniform(8.0, 10.0), 3)
            },
            "gyro": {
                "x": round(random.uniform(-5.0, 5.0), 3),
                "y": round(random.uniform(-5.0, 5.0), 3),
                "z": round(random.uniform(-5.0, 5.0), 3)
            }
        },
        "vibration": {
            "level": round(random.uniform(0.0, 10.0), 2)
        },
        "gps": {
            "latitude": round(random.uniform(18.0, 19.0), 6),
            "longitude": round(random.uniform(73.0, 74.0), 6),
            "altitude": round(random.uniform(400.0, 600.0), 2)
        }
    }

def main():
    print(f"Starting mock data generator. Writing to {LOG_FILE}")
    history = []
    
    # Optional: Clear previous logs on startup
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)
        
    while True:
        data = generate_mock_data()
        history.append(data)
        
        try:
            with open(LOG_FILE, 'w') as f:
                json.dump(history, f, indent=4)
            print(f"Updated data at {time.strftime('%H:%M:%S')}. Total records: {len(history)}")
        except Exception as e:
            print(f"Error writing to file: {e}")
        
        time.sleep(1) # Update every second

if __name__ == "__main__":
    main()
