import socket

server = "127.0.0.1"
port = 1024

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((server, port))

message = "This is a message from CS361" 
clientSocket.send(message.encode())