import socket
import threading
import queue
import rsa

# Generate public and private keys for the server
public_key, private_key = rsa.newkeys(1024)
clients = {}
messages = queue.Queue()

# Create and bind the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('localhost', 9999))

def receive():
    while True:
        try:
            message, address = server.recvfrom(2048)
            messages.put((message, address))
        except Exception as e:
            print(f"Error receiving message: {e}")

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            try:
                decoded_message = message.decode()
                if decoded_message.startswith("KEY:"):
                    public_key_str = decoded_message[len("KEY:"):]
                    clients[addr] = rsa.PublicKey.load_pkcs1(public_key_str.encode())
                    server.sendto(f"SERVER_KEY:{public_key.save_pkcs1().decode()}".encode(), addr)
                elif decoded_message.startswith("WELCOME :"):
                    name = decoded_message.split(":")[1].strip()
                    for client in clients.keys():
                        if client != addr:
                            server.sendto(f"{name} joined!".encode(), client)
                else:
                    raise UnicodeDecodeError  # If not a key or welcome message, raise error to be handled as encrypted
            except (UnicodeDecodeError, ValueError):
                if addr in clients:
                    try:
                        decrypted_message = rsa.decrypt(message, private_key).decode()
                        print(f"{decrypted_message}")  # Display the message normally
                        for client, pub_key in clients.items():
                            if client != addr:
                                encrypted_message = rsa.encrypt(decrypted_message.encode(), pub_key)
                                server.sendto(encrypted_message, client)
                    except Exception as e:
                        print(f"Error decrypting or sending message from {addr}: {e}")

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)
t1.start()
t2.start()
