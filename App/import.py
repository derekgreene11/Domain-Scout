# Name: Derek Greene
# OSU Email: greenede@oregonstate.edu
# Course: CS361 - Software Engineering I
# Description: Micro-service to handle exporting SQL dump from Domain Scout database. Service is initiated from Domain Scout through a TCP socket. Upon initiation, SQL dump is retrieved from API at https://derekrgreene.com/ct-data/api/export-dump 
# and saved to local file system. The file is saved to the 'backups/' directory in the project root. Upon successful fetch, the file name and path are sent back to Domain Scout over a TCP socket. 

import requests
import socket
import os

# Class to handle importing SQL dump to Domain Scout database
class Import:
    def __init__(self):
        self.API_URL = "https://derekrgreene.com/ct-data/api/import-dump"
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
    Method to import SQL dump to API.
    Parameters: clientSocket: object
    Returns: None
    """
    def importSQL(self, clientSocket):
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(self.API_URL, files=files)
            
            if response.status_code == 200:
                print(f"Imported SQL dump {file_path}")
                msg = f"{file_path} has been imported successfully"
                clientSocket.send(msg.encode())
            else:
                print(f"Failed to import SQL dump {file_path}")
                    

            
       
        #print(f"Exported SQL dump to {file_path}")

            


    """
    Method to loop and run export micro-service.
    Parameters: None
    Returns: None
    """
    def run(self):
        self.setupSocket()
            
        while True:
            clientSocket = self.awaitStart()
            self.importSQL(clientSocket)
            clientSocket.close()

client = Import()
client.run()

