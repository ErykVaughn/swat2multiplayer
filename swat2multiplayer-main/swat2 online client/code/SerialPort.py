import serial
import threading

class SerialPort:
    def __init__(self, com_port, baudrate=9600, timeout=1):
        """Initialize the serial port."""
        self.com_port = com_port
        self.baudrate = baudrate
        self.ser = serial.Serial(com_port, baudrate, timeout=timeout)
        self.lock = threading.Lock()  # Prevent conflicts when accessing the port

    def read_from_com(self):
        """Reads binary data from the COM port and returns it."""
        while True:
            with self.lock:
                if self.ser.in_waiting > 0:
                    data = self.ser.read(self.ser.in_waiting)  # Read available bytes
                    print(f"[{self.com_port}] Received: {data.hex()}")  # Print as hex
                    return data  # Return binary data

    def write_to_com(self, data):
        """Writes binary data to the COM port."""
        with self.lock:
            self.ser.write(data)
            print(f"[{self.com_port}] Sent: {data.hex()}")  # Print as hex

    def close(self):
        """Closes the serial connection."""
        self.ser.close()

# Example usage:
if __name__ == "__main__":
    serial_port = SerialPort("COM1")  # Change to your COM port

    # Start the read method in a thread
    read_thread = threading.Thread(target=serial_port.read_from_com, daemon=True)
    read_thread.start()

    # Example write operation (send some binary data)
    serial_port.write_to_com(b'\xAD\x00\x01\x02\x03')

    # Keep the script running
    read_thread.join()
