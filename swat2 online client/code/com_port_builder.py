import serial
import time
import subprocess

com0com_path = r"C:\Users\Eryk\Desktop\swat2 online client\setupc.exe"

def build_virtual_ports(serial1,serial2):
    try:
        result = subprocess.run([com0com_path, "list"], shell=True, capture_output=True, text=True)
        if serial1 in result.stdout and serial2 in result.stdout:
                print("[+] Virtual ports already exist. Skipping installation.")
                return True
        
        if subprocess.run([com0com_path, "install", f"PortName={serial1}", f"PortName={serial2}"], shell=True, capture_output=True, text=True).returncode == 0:
            print(f"[+] Virtual serial port {serial1} - {serial2} creating.")
            return True
        else:
            print(f"[ERROR] Failed to create virtual ports: {e}")
            return False
           
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}") 
        return False
    

def main():
    try:
        build_virtual_ports("COM1","COM3")
        build_virtual_ports("COM2","COM4")
    except serial.SerialException as e:  # Correct exception handling
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
