# Name: Derek Greene
# OSU Email: greenede@oregonstate.edu
# Course: CS361 - Software Engineering I
# Description: Micro-service to handle exporting SQL dump from Domain Scout database. Service is initiated from Domain Scout through a TCP socket. Upon initiation, SQL dump is retrieved from API at https://derekrgreene.com/ct-data/api/export-dump 
# and saved to local file system. The file is saved to the 'backups/' directory in the project root. Upon successful fetch, the file name and path are sent back to Domain Scout over a TCP socket. 

import requests
import socket
import os

# Class to handle exporting SQL dump from Domain Scout database
class Export:
    def __init__(self):
        self.API_URL = "https://derekrgreene.com/ct-data/api/export-dump"
        self.SAVE_DIR = "backups/"
        self.server = "127.0.0.1"
        self.port = 1024
        self.hostSocket = None
    
    """
    Method to create and bind socket to server/port.
    Parameters: None
    Returns: None
    """
    def setupSocket(self):
        self.hostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostSocket.bind((self.server, self.port))
        self.hostSocket.listen(5)

        print(f"Export micro-service listening on {self.server}:{self.port}")
    
    """
    Method to await export requests from Domain Scout.
    Parameters: None
    Returns: clientSocket: object
    """
    def awaitStart(self):
        try:
            clientSocket, clientAddr = self.hostSocket.accept()
            return clientSocket
        except Exception as e:
            return None    
    
    """
    Method to export SQL dump from API and save to local file system.
    Parameters: clientSocket: object
    Returns: None
    """
    def exportSQL(self, clientSocket):
        response = requests.get(self.API_URL)

        if response.status_code == 200:
            if not os.path.exists(self.SAVE_DIR):
                os.makedirs(self.SAVE_DIR)

            content_disposition = response.headers.get('Content-Disposition')
            filename = content_disposition.split('filename=')[1].strip('"') if content_disposition else 'backup.sql'
    
            file_path = os.path.join(self.SAVE_DIR, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)

            msg = f"{filename} has been downloaded successfully to {file_path}"
            clientSocket.send(msg.encode())
            print(f"Exported SQL dump to {file_path}")

    """
    Method to loop and run export micro-service.
    Parameters: None
    Returns: None
    """
    def run(self):
        self.setupSocket()
            
        while True:
            clientSocket = self.awaitStart()
            self.exportSQL(clientSocket)
            clientSocket.close()

client = Export()
client.run()