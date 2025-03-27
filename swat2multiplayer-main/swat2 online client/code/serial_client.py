import socket
import select
from SerialPort import SerialPort  # Import SerialPort class

def tcp_client(server_ip="192.168.1.49", server_port=5000, com_port="COM2"):
    """Real-time TCP client that connects to a server and communicates with a COM port."""
    serial_port = SerialPort(com_port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((server_ip, server_port))
            client_socket.setblocking(False)  # Set non-blocking mode
            print(f"[TCP CLIENT] Connected to {server_ip}:{server_port}")

            while True:
                # Use select to handle multiple I/O sources without blocking
                readable, _, _ = select.select([client_socket], [], [], 0.01)

                # Check for incoming TCP data
                if client_socket in readable:
                    response = client_socket.recv(1024)
                    if not response:
                        print("[TCP CLIENT] Server closed connection.")
                        break
                    print(f"[TCP CLIENT] Received from TCP Server: {response.hex()}")

                    # Write received data to COM port
                    serial_port.write_to_com(response)

                # Check if there is data from the Serial Port
                data = serial_port.read_from_com()
                if data:
                    print(f"[TCP CLIENT] Read from COM: {data.hex()}")
                    client_socket.sendall(data)  # Send serial data to TCP server
                    print(f"[TCP CLIENT] Sent to TCP Server: {data.hex()}")

        except Exception as e:
            print(f"[ERROR] {e}")

        finally:
            client_socket.close()
            serial_port.close()
            print("[TCP CLIENT] Connection closed.")

if __name__ == "__main__":
    tcp_client(server_ip="192.168.1.49", server_port=5000, com_port="COM2")  # Adjust as needed
