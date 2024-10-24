

import socket

server = "127.0.0.1"
port = 1024

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((server, port))
serverSocket.listen(1)

print("Server running on 127.0.0.1:1024")

clientSocket, clientAddr = serverSocket.accept()
msg = clientSocket.recv(1024).decode()
print(msg)

clientSocket.close()
serverSocket.close()