from socket import *
import os
from time import clock
import struct

def start():
    # Ask for command from client. Only progresses if connected.
    print("Options: CONN, UPLD, DWLD, LIST, DELF, QUIT")
    message = input("prompt user for operation: ").upper()
    if message == "CONN":
        print("connected")
        run()
    else:
        print("Must be connected to server")
        start()

def run():
    # Connects to server on port 12000
    serverAddress = ("localhost", 12000)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.connect(serverAddress)

    packer = struct.Struct('i')

    while True:
        # Client prompted for command
        print("Options: CONN, UPLD, DWLD, LIST, DELF, QUIT")
        message = input("prompt user for operation: ")
        serverSocket.sendall(message.encode())
        # If determines correct command to undertake
        if message.upper() == "UPLD":
            # Asks for file name
            print("UPLOAD")
            file = ""
            valid = False
            list = [f for f in os.listdir('.')]
            while not valid:
                # Does not advance until a valid file is named
                file = input("Valid file name (inc. extension): ")
                for i in list:
                    if file == i:
                        valid = True
            length = len(file)
            # Send file name length and file name
            serverSocket.send(packer.pack(length))
            serverSocket.send(file.encode())
            stats = os.stat(file)
            size = stats.st_size
            # Sends file size
            serverSocket.send(packer.pack(size))
            size = int(size)
            f = open(file, 'rb')
            sent = 0
            while sent < size:
                # Sends file in chunks of 1024 bytes
                part = f.read(1024)
                serverSocket.send(part)
                sent += 1024
            f.close()
            time = serverSocket.recv(8).decode()
            sizeTransferred = serverSocket.recv(8).decode()
            # Recieves time and displays success
            print(" ")
            print("Transfer Complete")
            print("Time taken: " + time + "s")
            print("size transfered: " + sizeTransferred + " bytes")

        elif message.upper() == "LIST":
            print("LIST")
            # Recieves size of list
            size = packer.unpack(serverSocket.recv(4))[0]
            list = ""
            got = 0
            start = clock()
            while got < size:
                # Recieves list in 1024 byte chunks
                new = serverSocket.recv(1024).decode()
                list += new
                got += 1024
            time = clock() - start
            list = list.split(':')
            # List is a string, split into list by ':'
            del list[-1]
            print("Files and Directories: ")
            for i in list:
                # Print list item
                print(i)
            print(" ")
            print("Time taken: " + str(time)[:8] + "s")
            print("size transfered: " + str(size) + " bytes")

        elif message.upper() == "DWLD":
            print("DOWNLOAD")
            # Prompt user for file name
            file = input("File to download (inc. extension): ")
            size = len(file)
            # Send file name and length to server
            serverSocket.send(packer.pack(size))
            serverSocket.send(file.encode())
            # Recieve int reply
            reply = packer.unpack(serverSocket.recv(4))[0]
            if reply == -1:
                print("File does not exist")
                # Abort if -1 reply
            else:
                fileSize = reply
                transferred = 0
                start = clock()
                with open(file, 'wb') as f:
                    # Open file to write to
                    while transferred < fileSize:
                        # Write to file in 1024 byte chunks
                        data = serverSocket.recv(1024)
                        transferred += 1024
                        f.write(data)
                    f.close()
                time = clock() - start
                # Prints time taken and file size
                print("Success")
                print("Time taken: " + str(time)[:8] + "s")
                print("size transfered: " + str(fileSize) + " bytes")

        elif message.upper() == "DELF":
            print("DELETE FILE")
            # Prompts for file to delete
            file = input("File to delete (inc. extension): ")
            size = len(file)
            # Send file name size and name to server
            serverSocket.send(packer.pack(size))
            serverSocket.send(file.encode())
            # Recieve confirmation file exists
            reply = packer.unpack(serverSocket.recv(4))[0]
            if reply == -1:
                # File doesn't exist if -1
                print("The file does not exist on server")
            else:
                decide = ""
                # File exists
                # Prompt for confirmation
                while decide != "YES" and decide != "NO":
                    decide = input("Confirm Deletion (Yes/No): ")
                    decide = decide.upper()
                # Send confirmationto delete to the server
                serverSocket.send(decide.encode())
                if decide == "YES":
                    # Print confirmation that server has deleted the file
                    print(serverSocket.recv(19).decode())
                else:
                    print("Delete abandoned by the user!")
        elif message.upper() == "QUIT":
            print("Session terminated")
            #Close socket and break loop (Ends client connection)
            serverSocket.close()
            break

start()