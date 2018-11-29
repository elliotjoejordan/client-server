READ ME

Client and Server use port 12000. port 12000 must be clear for client and server to use.


Included Files:

In client directory:
client.py
upload.txt

In server directory:
server.py
LargeFile.mp4
MediumFile.pdf
SmallFile.txt

To Run:

In a terminal, type: 'python3 server.py'
This starts the server.

In a seperate terminal, type: 'python3 client.py'
This will start the client.


Client will be prompted with input.
use 'CONN' to connect to server.

To run a command, enter the correct 4 letter code (not case sensitive).

When prompted for a file name (ie. in download, type full name):
eg. 'upload.txt'.

When finished, 'QUIT' to close client. abort server.

UPLD:
Enter file name. Client sends file to server and file is saved in server directory.

DWLD:
Enter file name. Client recieves file from server and saves in current directory.

LIST:
Server lists all files in server directory (excluding server.py and .DS_Store).

DELF:
Client enters file name to delete, server checks for file, asks client to confirm before deleting.

QUIT: 
Closes client and returns server to listening state for next client.