import socket
from SerialPort import SerialPort  # Import SerialPort class

def tcp_client(server_ip="192.168.1.49", server_port=5000, com_port="COM2"):
    """TCP client that connects to the server and handles COM port communication."""
    serial_port = SerialPort(com_port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((server_ip, server_port))
            print(f"[TCP CLIENT] Connected to {server_ip}:{server_port}")

            while True:
                # Read from local COM port
                data = serial_port.read_from_com()
                if data:
                    print(f"[TCP CLIENT] Read from COM: {data.hex()}")

                    # Send to TCP server
                    client_socket.sendall(data)
                    print(f"[TCP CLIENT] Sent to TCP Server: {data.hex()}")

                # Receive response from TCP server
                response = client_socket.recv(1024)
                if response:
                    print(f"[TCP CLIENT] Received from TCP Server: {response.hex()}")

                    # Write to local COM port
                    serial_port.write_to_com(response)

        except Exception as e:
            print(f"[ERROR] {e}")

        finally:
            client_socket.close()
            serial_port.close()
            print("[TCP CLIENT] Connection closed.")

if __name__ == "__main__":
    tcp_client(server_ip="0.0.0.0", server_port=5000, com_port="COM2")  # Change COM port if needed
