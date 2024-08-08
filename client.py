import socket
import threading
import rsa
import random

# Generate public and private keys for the client
public_key, private_key = rsa.newkeys(1024)
server_public_key = None

# Create and bind the client socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))
name = input("Nickname: ")

def receive():
    global server_public_key
    while True:
        try:
            message, _ = client.recvfrom(2048)
            if message.startswith(b"SERVER_KEY:"):
                server_public_key = rsa.PublicKey.load_pkcs1(message[len("SERVER_KEY:"):])
            else:
                decrypted_message = rsa.decrypt(message, private_key).decode()
                print(decrypted_message)  # Display the message normally
        except Exception as e:
            print(f"Error receiving message: {e}")

t = threading.Thread(target=receive)
t.start()

# Send the client's public key to the server
client.sendto(f"KEY:{public_key.save_pkcs1().decode()}".encode(), ("localhost", 9999))
client.sendto(f"WELCOME :{name}".encode(), ("localhost", 9999))

while True:
    message = input(" ")
    if message == "!q":
        exit()
    else:
        if server_public_key:
            encrypted_message = rsa.encrypt(f"{name}: {message}".encode(), server_public_key)
            client.sendto(encrypted_message, ("localhost", 9999))
        else:
            print("Waiting for server's public key...")
