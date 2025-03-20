import serial
import socket
import threading

# Configuration
TCP_IP = "0.0.0.0"  # Listen on all interfaces
BASE_TCP_PORT = 5000  # Starting TCP port
BASE_COM_PORT = "COM"  # Base COM port name
BAUDRATE = 9600
NUM_PLAYERS = 1  # Number of players (each player gets a TCP & COM port)


def handle_client(tcp_conn, com_port):
    """
    Handles communication between a TCP client and the assigned COM port.
    """
    try:
        ser = serial.Serial(com_port, BAUDRATE, timeout=1)
        print(f"[SERVER] Opened {com_port} for TCP connection.")

        while True:
            # Read from COM and send to TCP
            if ser.in_waiting:
                data = ser.readline().decode().strip()
                print(f"[{com_port}] Sending to TCP: {data}")
                tcp_conn.sendall((data + "\n").encode())

            # Read from TCP and send to COM
            tcp_data = tcp_conn.recv(1024).decode().strip()
            if tcp_data:
                print(f"[{com_port}] Received from TCP: {tcp_data}")
                ser.write((tcp_data + "\n").encode())

    except Exception as e:
        print(f"[ERROR] {com_port} - {e}")
    finally:
        ser.close()
        tcp_conn.close()
        print(f"[SERVER] Closed {com_port} and TCP connection.")


def start_server(num_players):
    """
    Starts a TCP server that opens multiple ports for multiple players.
    """
    for i in range(num_players):
        tcp_port = BASE_TCP_PORT + i
        com_port = f"{BASE_COM_PORT}{i+3}"  # Example: COM1, COM2, COM3

        threading.Thread(target=start_tcp_listener, args=(tcp_port, com_port), daemon=True).start()


def start_tcp_listener(tcp_port, com_port):
    """
    Listens for incoming TCP connections on a specific port.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, tcp_port))
    server_socket.listen(1)
    print(f"[LISTENING] TCP {tcp_port} waiting for connection...")

    while True:
        conn, addr = server_socket.accept()
        print(f"[CONNECTED] {addr} on TCP {tcp_port} -> {com_port}")
        threading.Thread(target=handle_client, args=(conn, com_port), daemon=True).start()


if __name__ == "__main__":
    print("[SERVER] Starting...")
    start_server(NUM_PLAYERS)
    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")