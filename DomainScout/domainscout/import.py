# Name: Derek Greene
# OSU Email: greenede@oregonstate.edu
# Course: CS361 - Software Engineering I
# Description: Micro-service to handle importing SQL dump from 'backups' directory to Domain Scout database. Service is initiated from Domain Scout through a TCP socket. Upon initiation, SQL dump is retrieved from 'backups' directory and sent to API at https://derekrgreene.com/ct-data/api/import-dump 
# A message indicating success or failure it sent from the micro-service back to Domain Scout over a TCP socket. 

import requests
import socket
import os

# Class to handle importing SQL dump to Domain Scout database
class Import:
    def __init__(self):
        self.API_URL = "https://derekrgreene.com/ct-data/api/import-dump"
        self.BACKUP_DIR = "backups/"
        self.server = "127.0.0.1"
        self.port = 1026
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

        print(f"Import micro-service listening on {self.server}:{self.port}")

    """
    Method to await import requests from Domain Scout.
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
    Method to find most recent SQL dump file in 'backups' directory.
    Parameters: None
    Returns: filePath: str
    """
    def findSQLFile(self):
        sqlFiles = [f for f in os.listdir(self.BACKUP_DIR) if f.endswith('.sql')]
        
        if not sqlFiles:
            return None
        
        sqlFiles.sort(reverse=True)
        return os.path.join(self.BACKUP_DIR, sqlFiles[0])

    """
    Method to import SQL dump to API.
    Parameters: clientSocket: object, filePath: str
    Returns: None
    """
    def importSQL(self, filePath, clientSocket):
        with open(filePath, 'rb') as f:
            files = {'file': (os.path.basename(filePath), f)}
            response = requests.post(self.API_URL, files=files)
            
            if response.status_code == 200:
                print(f"Imported SQL dump {filePath}")
                msg = f"{filePath} has been imported successfully"
                clientSocket.send(msg.encode())
            else:
                print(f"Failed to import SQL dump {filePath}")
                    
    """
    Method to loop and run import micro-service.
    Parameters: None
    Returns: None
    """
    def run(self):
        self.setupSocket()
            
        while True:
            clientSocket = self.awaitStart()
            filePath = self.findSQLFile()
            if filePath:
                self.importSQL(filePath, clientSocket)
                clientSocket.close()
            else:
                print("No SQL dump found to import")
                msg = "No SQL dump found to import!"
                clientSocket.send(msg.encode())
            clientSocket.close()

client = Import()
client.run()
