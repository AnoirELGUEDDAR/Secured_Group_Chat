import socket
import threading
import queue
import rsa

public_key, private_key = rsa.newkeys(1024)
clients = {}  # Dictionary to store client address and public key

messages = queue.Queue()  # Queue to store messages received from clients
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('localhost', 9999))  # bind the server to the specified IP and port


def receive():  # receive messages from clients and put them into the queue
    while True:
        try:
            message, address = server.recvfrom(
                1024)  # Receives a message of up to 1024 bytes and the address it came from
            messages.put((message, address))  # put the received message and address as a tuple into the queue
        except:
            pass


def broadcast():  # take the messages from queue and broadcast them to all clients
    while True:
        while not messages.empty():  # check if there are any messages in the queue
            message, addr = messages.get()  # get the message and address from the queue

            if addr not in clients:
                clients[addr] = None

            try:
                decoded_message = message.decode()

                if decoded_message.startswith("KEY:"):  # If the message contains a public key
                    client_public_key = rsa.PublicKey.load_pkcs1(decoded_message[4:].encode())
                    clients[addr] = client_public_key
                else:
                    if decoded_message.startswith("WELCOME :"):  # If the client is new
                        name = decoded_message.split(":")[1]  # to detect the name
                        for client in clients:
                            server.sendto(f"{name} joined!".encode(), client)
                    else:
                        for client, client_public_key in clients.items():
                            if client_public_key is not None:
                                encrypted_message = rsa.encrypt(message, client_public_key)
                                server.sendto(encrypted_message, client)
            except UnicodeDecodeError:
                # if the message cannot be decoded,just send it to all clients as it is
                for client in clients:
                    server.sendto(message, client)
            except Exception as e:
                print(f"Error: {e}")
                clients.pop(client)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(
    target=broadcast)  # Threading allows you to have different parts of your process run at the same time
t1.start()
t2.start()
