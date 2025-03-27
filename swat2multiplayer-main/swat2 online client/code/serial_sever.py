import socket
import select
from SerialPort import SerialPort  # Import SerialPort class

def tcp_server(host="192.168.1.49", port=5000, com_port="COM1"):
    """TCP server that handles real-time bidirectional communication between TCP and Serial Port."""
    serial_port = SerialPort(com_port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"[TCP SERVER] Listening on {host}:{port}")

        conn, addr = server_socket.accept()
        print(f"[TCP SERVER] Connection from {addr}")

        conn.setblocking(False)  # Set non-blocking mode for TCP socket

        try:
            while True:
                # Use select to wait for incoming TCP or Serial data
                readable, _, _ = select.select([conn], [], [], 0.01)  # Non-blocking wait
                
                # Check if there is incoming TCP data
                if conn in readable:
                    data = conn.recv(1024)
                    if not data:
                        break  # Exit if connection is closed
                    print(f"[TCP SERVER] Received from TCP: {data.hex()}")

                    # Write to COM port
                    serial_port.write_to_com(data)

                # Check if there is data from the Serial Port
                response = serial_port.read_from_com()
                if response:
                    conn.sendall(response)  # Send to TCP client
                    print(f"[TCP SERVER] Sent to TCP: {response.hex()}")

        except Exception as e:
            print(f"[ERROR] {e}")

        finally:
            conn.close()
            serial_port.close()
            print("[TCP SERVER] Connection closed.")

if __name__ == "__main__":
    tcp_server(host="192.168.1.101", port=5000, com_port="COM1")  # Change COM port if needed
