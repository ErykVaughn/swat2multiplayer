import sys
import serial
import socket
import threading
import serial.tools.list_ports
import subprocess
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget

# Configurable settings
BAUDRATE_OPTIONS = [9600, 14400, 19200, 38400, 56000, 57600, 115200, 128000, 256000]
SERIAL_PORT = "COM3"  # Change based on OS
TCP_PORT = 5000       # Default port for multiplayer

def ensure_virtual_serial_port():
    """ Ensures a virtual serial port is available using com0com """
    ports = [port.device for port in com_port_builder.tools.list_ports.comports()]
    
    if SERIAL_PORT not in ports:
        print(f"[!] Virtual {SERIAL_PORT} not found. Checking com0com setup...")
        if os.name == "nt":
            com0com_path = r"C:\\Program Files (x86)\\com0com\\setupc.exe"
            if not os.path.exists(com0com_path):
                print("[ERROR] com0com not found. Please install it first.")
                return False
            
            try:
                # Check if any ports already exist
                result = subprocess.run([com0com_path, "list"], shell=True, capture_output=True, text=True)
                if f"CNCA0" in result.stdout or f"CNCA1" in result.stdout:
                    print("[+] Virtual ports already exist. Skipping installation.")
                    return True

                # Install virtual COM3-COM4 pair
                subprocess.run([com0com_path, "install", "PortName=COM3", "PortName=COM4"], shell=True, check=True)
                print("[+] Virtual serial port COM3-COM4 created.")
                
                # Wait and recheck
                time.sleep(2)
                ports = [port.device for port in com_port_builder.tools.list_ports.comports()]
                if SERIAL_PORT not in ports:
                    print("[ERROR] COM3 still not detected. Exiting.")
                    return False
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Failed to create virtual ports: {e}")
                return False
        else:
            os.system("socat -d -d pty,raw,echo=0 pty,raw,echo=0 &")
    
    return True

def handle_client(client_socket, ser):
    """ Handles incoming TCP data and sends it to the serial port """
    print(f"[+] New connection from {client_socket.getpeername()}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"[TCP] Received: {data.decode('utf-8')}")
            ser.write(data)

            serial_data = ser.readline().decode('utf-8').strip()
            if serial_data:
                print(f"[SERIAL] Received: {serial_data}")
                client_socket.send(serial_data.encode())
    except Exception as e:
        print(f"[-] Connection error: {e}")
    finally:
        client_socket.close()
        print("[*] Client disconnected")

def start_server():
    """ Starts the server to host a multiplayer session """
    if not ensure_virtual_serial_port():
        return  # Exit if the port cannot be created
    
    print(f"[*] Opening serial port {SERIAL_PORT} at {BAUDRATE_OPTIONS[0]} baud")
    
    try:
        ser = com_port_builder.Serial(SERIAL_PORT, BAUDRATE_OPTIONS[0], timeout=1)
    except com_port_builder.SerialException as e:
        print(f"[ERROR] Unable to open {SERIAL_PORT}: {e}")
        return

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", TCP_PORT))
    server.listen(5)
    print(f"[*] Listening for TCP connections on 0.0.0.0:{TCP_PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, ser))
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[*] Shutting down server")
    finally:
        ser.close()
        server.close()

def connect_to_host(host_ip):
    """ Connects to the SWAT2 multiplayer host over the network """
    if not ensure_virtual_serial_port():
        return
    
    print(f"[*] Opening serial port {SERIAL_PORT} at {BAUDRATE_OPTIONS[0]} baud")
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE_OPTIONS[0], timeout=1)
    except serial.SerialException as e:
        print(f"[ERROR] Unable to open {SERIAL_PORT}: {e}")
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host_ip, TCP_PORT))
        print(f"[+] Connected to SWAT2 host at {host_ip}:{TCP_PORT}")

        while True:
            serial_data = ser.readline().decode('utf-8').strip()
            if serial_data:
                print(f"[SERIAL] Sending: {serial_data}")
                client.send(serial_data.encode())

            tcp_data = client.recv(1024)
            if tcp_data:
                print(f"[TCP] Received: {tcp_data.decode('utf-8')}")
                ser.write(tcp_data)
    except Exception as e:
        print(f"[-] Connection error: {e}")
    finally:
        ser.close()
        client.close()

class Swat2UI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Available Games:")
        layout.addWidget(self.label)
        
        self.gameList = QListWidget()
        layout.addWidget(self.gameList)
        
        self.refreshButton = QPushButton("Refresh Games")
        self.refreshButton.clicked.connect(self.refresh_games)
        layout.addWidget(self.refreshButton)
        
        self.hostButton = QPushButton("Host Game")
        self.hostButton.clicked.connect(self.host_game)
        layout.addWidget(self.hostButton)
        
        self.connectButton = QPushButton("Connect to Game")
        self.connectButton.clicked.connect(self.connect_game)
        layout.addWidget(self.connectButton)
        
        self.setLayout(layout)
        self.setWindowTitle("SWAT2 Multiplayer")
        self.show()

    def refresh_games(self):
        self.gameList.clear()
        self.gameList.addItem("192.168.1.2 (Example Host)")

    def host_game(self):
        threading.Thread(target=start_server, daemon=True).start()

    def connect_game(self):
        selected_item = self.gameList.currentItem()
        if selected_item:
            host_ip = selected_item.text().split(" ")[0]
            threading.Thread(target=connect_to_host, args=(host_ip,), daemon=True).start()
        else:
            self.label.setText("Select a game first!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Swat2UI()
    sys.exit(app.exec_())