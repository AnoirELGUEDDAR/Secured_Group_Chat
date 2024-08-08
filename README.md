![image](https://github.com/user-attachments/assets/969a470b-1ef8-44fa-96bb-419174ae53d2)
***In WIRESHARK,as you see the message is encrypted***
![image](https://github.com/user-attachments/assets/df037efd-87a1-4f3b-a76f-b97953c88ee4)


This project implements a peer-to-peer (P2P) group chat application that prioritizes security using RSA encryption. It enables multiple users to connect and communicate directly with each other in real-time without relying on a central server.

## Security Benefits:

Confidentiality: RSA encryption guarantees that only the sender and intended recipients can access the message content.
Privacy: The decentralized nature eliminates the risk of a single point of failure or compromise associated with central servers.
Integrity: RSA signatures (not implemented in this basic version) could be used to verify the authenticity of messages and prevent tampering.

## How to Use:
### 1.Prerequisites:
Ensure you have Python 3.x installed.
Install the rsa library using pip install rsa.
### 2.Start the Server: 
Run python server.py in a terminal.
### 3.Start Clients: 
Open multiple terminals and run python client.py in each. Enter a nickname for each user.
### 4.Chat: 
Type messages and press Enter to send them.
### 5.Exit: 
Type !q to quit.
## Potential Enhancements:
### Message Authentication: 
Implement RSA signatures to verify message authenticity.
### Key Management: 
Incorporate more robust key management strategies for larger-scale applications.
### User Interface: 
Develop a graphical user interface (GUI) for a more user-friendly experience.
### Direct Messaging: 
Enable private messaging between individual users.










