import serial

# Configuration
COM_PORT = "COM1"  # Change this to your port (e.g., "COM3" on Windows or "/dev/ttyUSB0" on Linux)
BAUDRATE = 9600

try:
    with serial.Serial(COM_PORT, BAUDRATE, timeout=1) as ser:
        print(f"Connected to {COM_PORT}. Waiting for data...")
        
        # Clear any existing data in the buffer
        ser.reset_input_buffer()

        while True:
            if ser.in_waiting > 0:  # Only read if there's new data
                data = ser.readline()  # Read until newline
                if data:  # Ensure it's not empty
                    print("")
                    print(f"Raw Bytes: {data}")
                    print(f"Hex: {data.hex()}")
                    print(f"Int Values: {[b for b in data]}")
                    print("")
                else:
                    print("No new data received.")

except serial.SerialException as e:
    print(f"Error: {e}")