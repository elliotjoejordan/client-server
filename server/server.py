from socket import *
import os
from time import *
import struct

def start():
    # Starts by opening connection
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("localhost", serverPort))
    serverSocket.listen(1)

    # Waits for client connection

    packer = struct.Struct('i')

    print("wait for connection")
    # Accepts connection
    connectionSocket, addr = serverSocket.accept()
    while True:
        print("wait for operation from client")
        # Read opperation
        code = connectionSocket.recv(4).decode().upper()
        if code == "CONN":
            print("connected")
        elif code == "UPLD":
            print("UPLOAD")
            length = packer.unpack(connectionSocket.recv(4))[0]
            # Read in length of file name
            # Read in file name and size
            name = connectionSocket.recv(length).decode()
            size = packer.unpack(connectionSocket.recv(4))[0]
            print("ready to receive")
            transferred = 0
            startTime = clock()
            with open(name, 'wb') as f:
                # Open file to upload/write to
                while transferred < size:
                    data = connectionSocket.recv(1024)
                    # Recieve and write data in 1024 byte chunks
                    transferred += 1024
                    f.write(data)
                f.close()
            timeTaken = clock() - startTime
            sizeTransferred = size
            # Send size transfered and time taken to client
            timeTaken = str(timeTaken)
            connectionSocket.send(timeTaken[:8].encode())
            connectionSocket.send(str(sizeTransferred).encode())

        elif code == "LIST":
            print("LIST")
            # Get list of files in directory
            list = [f for f in os.listdir('.')]
            listString = ""
            # Remove irrelevant files and add revelant ones to a string
            for item in list:
                if item == 'server.py':
                    list.remove(item)
                elif item == '.DS_Store':
                    list.remove(item)
                else:
                    # Separate list items in string by ':'
                    listString += item + ":"
            size = len(listString)
            # Send string length to client
            connectionSocket.send(packer.pack(size))

            sent = 0
            while sent < size:
                # Send string of list to client
                connectionSocket.send(listString.encode())
                sent += size

        elif code == "DWLD":
            print("DOWNLOAD")
            # Unpack and receive length of name and name of file to download
            length = packer.unpack(connectionSocket.recv(4))[0]
            name = connectionSocket.recv(length).decode()
            # Check if file exists and respond with either -1, or file size (32 bit int)
            list = [f for f in os.listdir('.')]
            if name not in list:
                connectionSocket.send(packer.pack(-1))
            else:
                stats = os.stat(name)
                fileSize = stats.st_size
                connectionSocket.send(packer.pack(fileSize))
                sent = 0
                with open(name, 'rb') as f:
                    # Open file and send in 1024 byte chunks
                    while sent < int(fileSize):
                        part = f.read(1024)
                        connectionSocket.send(part)
                        sent += 1024
                    f.close()

        elif code == "DELF":
            print("DELETE FILE")
            # Receive and unpack length of file name and receive file name
            length = packer.unpack(connectionSocket.recv(4))[0]
            name = connectionSocket.recv(length).decode()
            # Check if file exists, respond with -1 (does not) or 1 (does exist)
            list = [f for f in os.listdir('.')]
            if name not in list:
                connectionSocket.send(packer.pack(-1))
            else:
                connectionSocket.send(packer.pack(1))
                answer = connectionSocket.recv(4).decode()
                # Receive confirmation (Client wants to continue and delete)
                answer = answer.upper()
                if answer == "YES":
                    # Remove file
                    os.remove(name)
                    # Inform client success
                    connectionSocket.send(("Deletion successful").encode())
        elif code == "QUIT":
            # Disconnect client
            connectionSocket.close()
            print("wait for connection")
            # Server waits here for new client, returning to waiting for commands once one connects
            connectionSocket, addr = serverSocket.accept()
        else:
            print("INVALID command")

start()