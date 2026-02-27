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

def generate_large_history_bulk():
    print("Generating massive test log (JSON Lines format)...")
    
    # Generate 5,000 mock records instantly
    with open(LOG_FILE, 'w') as f:
        # We start the timestamp 5000 seconds ago
        base_time = time.time() - 5000 
        
        for i in range(5000):
            data = generate_mock_data()
            data['timestamp'] = base_time + i
            
            # Write as JSON Lines (one JSON object per line)
            f.write(json.dumps(data) + "\n")
            
    print(f"Generated 5,000 JSON line records at {LOG_FILE}")

if __name__ == "__main__":
    generate_large_history_bulk()
