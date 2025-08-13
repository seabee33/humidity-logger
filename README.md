# DHT11 Sensor Data Logger

A Python application for monitoring DHT11 temperature and humidity sensors on Raspberry Pi, with automatic data averaging and HTTP API integration.

## Features

- Monitor multiple DHT11 sensors simultaneously
- Collect readings every 2 seconds
- Calculate 60-second rolling averages
- Send averaged data to HTTP endpoint via JSON API
- Automatic startup service with systemd
- Comprehensive error handling and logging
- Graceful handling of sensor read failures

## Hardware Requirements

- Raspberry Pi (tested on Pi 3)
- DHT11 sensor modules (breakout board recommended)
- Jumper wires for connections

## Hardware Setup

### Sensor Wiring

Connect your DHT11 sensors to the Raspberry Pi GPIO pins:

**Sensor 1:**
- VCC → Pin 2 (5V)
- GND → Pin 6 (Ground)
- Data → Pin 7 (GPIO 4)

**Sensor 2:**
- VCC → Pin 2 (5V) - can share with Sensor 1
- GND → Pin 9 (Ground)
- Data → Pin 11 (GPIO 17)

> **Note:** If using DHT11 breakout boards, no external pull-up resistors are required.

## Software Installation

### Prerequisites

```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

### Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd dht11-sensor-monitor
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip3 install adafruit-circuitpython-dht RPi.GPIO requests
sudo apt install libgpiod2
```

4. **Configure the data endpoint:**
Edit `humid.py` and update the `SEND_URL` variable:
```python
SEND_URL = "http://your-server.com/api/sensor-data"
```

## Usage

### Manual Testing

```bash
# Activate virtual environment
source venv/bin/activate

# Run the sensor monitor
python3 humid.py
```

### Automatic Startup Service

1. **Make the startup script executable:**
```bash
chmod +x run_sensors.sh
```

2. **Test the startup script:**
```bash
./run_sensors.sh
```

3. **Create systemd service:**
```bash
sudo nano /etc/systemd/system/dht11-sensor.service
```

Add the following content:
```ini
[Unit]
Description=DHT11 Sensor Data Logger
After=network.target

[Service]
Type=simple
User=conor
WorkingDirectory=/home/conor
ExecStart=/home/conor/run_sensors.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

4. **Enable and start the service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable dht11-sensor.service
sudo systemctl start dht11-sensor.service
```

## Monitoring and Logs

### Service Status
```bash
# Check service status
sudo systemctl status dht11-sensor.service

# View application logs
tail -f sensor.log

# View systemd logs
sudo journalctl -u dht11-sensor.service -f
```

### Service Management
```bash
# Stop the service
sudo systemctl stop dht11-sensor.service

# Start the service
sudo systemctl start dht11-sensor.service

# Restart the service
sudo systemctl restart dht11-sensor.service

# Disable auto-start
sudo systemctl disable dht11-sensor.service
```

## API Data Format

The application sends JSON data to your configured endpoint every 60 seconds:

```json
{
  "timestamp": "2025-08-14T10:30:00.123456",
  "data": {
    "sensor1_temp_avg": 23.45,
    "sensor1_hum_avg": 65.23,
    "sensor2_temp_avg": 24.12,
    "sensor2_hum_avg": 63.87
  },
  "sample_count": 30,
  "window_seconds": 60
}
```

## Configuration

### Timing Settings
Edit `humid.py` to adjust timing parameters:

```python
SAMPLE_INTERVAL = 2  # seconds between readings
AVERAGE_WINDOW = 60  # seconds for averaging window
```

### Adding More Sensors
To add additional sensors, modify the initialization section:

```python
# Add new sensor
dht3 = adafruit_dht.DHT11(board.D27)  # GPIO 27

# Add corresponding data storage
sensor3_temp = deque(maxlen=SAMPLES_PER_AVERAGE)
sensor3_hum = deque(maxlen=SAMPLES_PER_AVERAGE)
```

## Troubleshooting

### Common Issues

**Import Error: No module named 'RPi'**
```bash
pip3 install RPi.GPIO
```

**Permission Denied on GPIO**
```bash
sudo usermod -a -G gpio $USER
# Log out and back in
```

**Service Won't Start**
- Check file paths in `run_sensors.sh`
- Verify virtual environment exists
- Check service logs: `sudo journalctl -u dht11-sensor.service`

**Sensor Read Errors**
- Verify wiring connections
- Check power supply (5V recommended)
- DHT11 sensors can be temperamental - occasional read errors are normal

### Log Files
- Application logs: `sensor.log`
- System logs: `sudo journalctl -u dht11-sensor.service`

## File Structure

```
dht11-sensor-monitor/
├── humid.py              # Main sensor monitoring script
├── run_sensors.sh        # Startup script with venv activation
├── sensor.log           # Application log file (created at runtime)
├── venv/                # Python virtual environment
└── README.md           # This file
```

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on Raspberry Pi hardware
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section above
- Review application logs in `sensor.log`
- Open an issue on GitHub with detailed error information and hardware setup
