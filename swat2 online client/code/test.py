import serial

# Serial Port Config
COM1 = "COM1"  # Server (Host)
COM2 = "COM2"
COM3 = "COM3"  # Client
COM4 = "COM4"
BAUDRATE = 9600


def main():
    try:
        ser1 = serial.Serial(COM1, BAUDRATE, timeout=1)
        ser2 = serial.Serial(COM2, BAUDRATE, timeout=1)
        ser3 = serial.Serial(COM3, BAUDRATE, timeout=1)
        ser4 = serial.Serial(COM4, BAUDRATE, timeout=1)

        # Send data to COM1
        ser1.write("heello com1".encode())  

        # Read responses
        response2 = ser2.readline().decode().strip()
        response3 = ser3.readline().decode().strip()
        response4 = ser4.readline().decode().strip()

        print(f"Response from COM2: {response2}")
        print(f"Response from COM3: {response3}")
        print(f"Response from COM4: {response4}")

    except serial.SerialException as e:
        print(f"Serial error: {e}")

    finally:
        # Close serial ports to prevent resource leaks
        if 'ser1' in locals(): ser1.close()
        if 'ser2' in locals(): ser2.close()
        if 'ser3' in locals(): ser3.close()
        if 'ser4' in locals(): ser4.close()


if __name__ == "__main__":
    main()
