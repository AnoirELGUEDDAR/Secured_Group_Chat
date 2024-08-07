import socket
import threading
import rsa
import random

public_key, private_key = rsa.newkeys(1024)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))
name = input("Nickname: ")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)  # _ is used to ignore the address
            decrypted_message = rsa.decrypt(message, private_key).decode()
            print(decrypted_message)
        except:
            pass

t = threading.Thread(target=receive)
t.start()

# Send public key to server
client.sendto(f"KEY:{public_key.save_pkcs1().decode()}".encode(), ("localhost", 9999))
client.sendto(f"WELCOME :{name}".encode(), ("localhost", 9999))  # Because for every client, the first message is a welcome message

while True:
    message = input(" ")
    if message == "!q":
        exit()
    else:
        encrypted_message = rsa.encrypt(f"{name}: {message}".encode(), public_key)
        client.sendto(encrypted_message, ("localhost", 9999))
