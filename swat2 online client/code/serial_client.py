import serial
import socket
import threading

# Configuration
SERVER_IP = "127.0.0.1"  # Change to the server's IP
BASE_TCP_PORT = 5000  # Base TCP port to connect
COM_PORT = "COM4"  # Change based on your system
BAUDRATE = 9600


def read_from_com_and_send_to_tcp(tcp_socket, ser):
    """
    Reads from the COM port and sends data to the server.
    """
    try:
        while True:
            if ser.in_waiting:
                data = ser.readline().decode().strip()
                print(f"[{COM_PORT}] Sending to TCP: {data}")
                tcp_socket.sendall((data + "\n").encode())
    except Exception as e:
        print(f"[ERROR] COM Read Error: {e}")


def read_from_tcp_and_send_to_com(tcp_socket, ser):
    """
    Reads from the TCP server and sends data to the COM port.
    """
    try:
        while True:
            data = tcp_socket.recv(1024).decode().strip()
            if data:
                print(f"[{COM_PORT}] Received from TCP: {data}")
                ser.write((data + "\n").encode())
    except Exception as e:
        print(f"[ERROR] TCP Read Error: {e}")


def start_client(server_ip, tcp_port, com_port):
    """
    Connects to the TCP server and starts data forwarding.
    """
    try:
        ser = serial.Serial(com_port, BAUDRATE, timeout=1)
        print(f"[CLIENT] Connected to {com_port}")

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((server_ip, tcp_port))
        print(f"[CLIENT] Connected to TCP {server_ip}:{tcp_port}")

        # Start bidirectional communication threads
        threading.Thread(target=read_from_com_and_send_to_tcp, args=(tcp_socket, ser), daemon=True).start()
        threading.Thread(target=read_from_tcp_and_send_to_com, args=(tcp_socket, ser), daemon=True).start()

        while True:
            pass  # Keep running
    except Exception as e:
        print(f"[ERROR] Client Error: {e}")
    finally:
        ser.close()
        tcp_socket.close()


if __name__ == "__main__":
    tcp_port = BASE_TCP_PORT  # Choose the appropriate TCP port
    start_client(SERVER_IP, tcp_port, COM_PORT)