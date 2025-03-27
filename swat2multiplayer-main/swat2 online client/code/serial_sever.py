import socket
from SerialPort import SerialPort  # Import SerialPort class

def tcp_server(host="192.168.1.49", port=5000, com_port="COM1"):
    """TCP server that handles reading/writing to a serial port."""
    serial_port = SerialPort(com_port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"[TCP SERVER] Listening on {host}:{port}")

        conn, addr = server_socket.accept()
        print(f"[TCP SERVER] Connection from {addr}")

        try:
            while True:
                # Receive data from TCP client
                data = conn.recv(1024)
                if not data:
                    break  # Exit loop if connection is closed
                print(f"[TCP SERVER] Received from TCP: {data.hex()}")

                # Write received data to COM port
                serial_port.write_to_com(data)

                # Read response from COM port
                response = serial_port.read_from_com()
                if response:
                    conn.sendall(response)  # Send response back to client
                    print(f"[TCP SERVER] Sent to TCP: {response.hex()}")

        except Exception as e:
            print(f"[ERROR] {e}")

        finally:
            conn.close()
            serial_port.close()
            print("[TCP SERVER] Connection closed.")

if __name__ == "__main__":
    tcp_server(host="0.0.0.0", port=5000, com_port="COM1")  # Change COM port if needed
