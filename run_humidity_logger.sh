#!/bin/bash

# DHT11 Sensor Data Logger Startup Script
# This script activates the virtual environment and runs the sensor monitoring script

USERNAME=username_here

# Configuration - Update these paths as needed
SCRIPT_DIR="/home/$USERNAME"
VENV_PATH="/home/$USERNAME/venv"
PYTHON_SCRIPT="humid.py"
LOG_FILE="/home/$USERNAME/sensor.log"

# Function to log messages with timestamp
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Change to script directory
cd "$SCRIPT_DIR" || {
    log_message "ERROR: Could not change to directory $SCRIPT_DIR"
    exit 1
}

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    log_message "ERROR: Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    log_message "ERROR: Python script not found at $SCRIPT_DIR/$PYTHON_SCRIPT"
    exit 1
fi

# Activate virtual environment and run script
log_message "Starting DHT11 sensor monitoring..."
log_message "Virtual environment: $VENV_PATH"
log_message "Python script: $SCRIPT_DIR/$PYTHON_SCRIPT"
log_message "Logs will be written to: $LOG_FILE"

# Source the virtual environment and run the script
source "$VENV_PATH/bin/activate" && {
    log_message "Virtual environment activated successfully"
    log_message "Running sensor script..."
    
    # Run the Python script and capture both stdout and stderr
    python3 "$PYTHON_SCRIPT" 2>&1 | while IFS= read -r line; do
        log_message "$line"
    done
    
} || {
    log_message "ERROR: Failed to activate virtual environment or run script"
    exit 1
}
