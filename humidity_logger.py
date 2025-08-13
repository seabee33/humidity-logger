import adafruit_dht board time requests json statistics
from collections import deque
from datetime import datetime 

# Configuration
SEND_URL = "http://server.com/"  # Replace with your URL
SAMPLE_INTERVAL = 2  # seconds
AVERAGE_WINDOW = 60  # seconds
SAMPLES_PER_AVERAGE = AVERAGE_WINDOW // SAMPLE_INTERVAL  # 30 samples

# Initialize DHT11 sensors
dht1 = adafruit_dht.DHT11(board.D4)  # pin 7 gpio 4
dht2 = adafruit_dht.DHT11(board.D17)  # pin 11 gpio 17

# Data storage for rolling averages
sensor1_temp = deque(maxlen=SAMPLES_PER_AVERAGE)
sensor1_hum = deque(maxlen=SAMPLES_PER_AVERAGE)
sensor2_temp = deque(maxlen=SAMPLES_PER_AVERAGE)
sensor2_hum = deque(maxlen=SAMPLES_PER_AVERAGE)

def read_sensors():
    """Read both sensors and return the values"""
    temp1 = hum1 = temp2 = hum2 = None
    
    try:
        temp1 = dht1.temperature
        hum1 = dht1.humidity
    except RuntimeError as e:
        print(f"Sensor 1 error: {e.args[0]}")
    
    try:
        temp2 = dht2.temperature
        hum2 = dht2.humidity
    except RuntimeError as e:
        print(f"Sensor 2 error: {e.args[0]}")
    
    return temp1, hum1, temp2, hum2

def calculate_averages():
    """Calculate averages from stored samples"""
    averages = {}
    
    if len(sensor1_temp) > 0:
        # Filter out None values before calculating average
        valid_temp1 = [x for x in sensor1_temp if x is not None]
        valid_hum1 = [x for x in sensor1_hum if x is not None]
        
        if valid_temp1:
            averages['sensor1_temp_avg'] = round(statistics.mean(valid_temp1), 2)
        if valid_hum1:
            averages['sensor1_hum_avg'] = round(statistics.mean(valid_hum1), 2)
    
    if len(sensor2_temp) > 0:
        valid_temp2 = [x for x in sensor2_temp if x is not None]
        valid_hum2 = [x for x in sensor2_hum if x is not None]
        
        if valid_temp2:
            averages['sensor2_temp_avg'] = round(statistics.mean(valid_temp2), 2)
        if valid_hum2:
            averages['sensor2_hum_avg'] = round(statistics.mean(valid_hum2), 2)
    
    return averages

def send_data(data):
    """Send averaged data to the specified URL"""
    try:
        payload = {
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'sample_count': len(sensor1_temp),
            'window_seconds': AVERAGE_WINDOW
        }
        
        response = requests.post(
            SEND_URL, 
            json=payload, 
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"Data sent successfully: {data}")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Network error sending data: {e}")
    except Exception as e:
        print(f"Error sending data: {e}")

# Main loop
print(f"Starting sensor monitoring...")
print(f"Sample interval: {SAMPLE_INTERVAL}s, Average window: {AVERAGE_WINDOW}s")
print(f"Will send averages every {SAMPLES_PER_AVERAGE} samples\n")

sample_count = 0

while True:
    # Read sensors
    temp1, hum1, temp2, hum2 = read_sensors()
    
    # Store readings (even if None - deque will handle it)
    sensor1_temp.append(temp1)
    sensor1_hum.append(hum1)
    sensor2_temp.append(temp2)
    sensor2_hum.append(hum2)
    
    sample_count += 1
    
    # Print current readings
    print(f"Sample {sample_count}: T1={temp1}°C H1={hum1}% | T2={temp2}°C H2={hum2}%")
    
    # Send averages every 60 seconds (30 samples)
    if sample_count % SAMPLES_PER_AVERAGE == 0:
        averages = calculate_averages()
        if averages:
            print(f"\n📊 60-second averages: {averages}")
            send_data(averages)
            print()
        else:
            print("No valid data to average :(")
    
    time.sleep(SAMPLE_INTERVAL)
