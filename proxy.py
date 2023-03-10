# Import socket module
from socket import *
#from google.colab import files
import os

# Set the path of the folder you want to create
folder_path = 'cache_folder'

# Create the folder if it does not exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

proxy_socket = socket(AF_INET, SOCK_STREAM)
print("Proxy socket created\n")

# Establish the port to be bound to and bind it to the server_socket #
proxy_socket.bind(("", 8888))
print("Socket binded to 8888\n")
# Start listening to allow socket to accept connection requests, 1 so that #
# it handles only one request at a time #
print("Socket starts listening\n")
proxy_socket.listen(1)
# Server should be up and running and listening to the incoming connections
while True:
    print('Ready to serve...')
    # Set up a new connection from the client
    # Accepts the connection being "listened" from the server socket ##
    connection_socket, addr = proxy_socket.accept()
    print("Proxy socket accepted connection, connection socket created\n")
    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except clause is executed
    try:
        # Receives the request message from the client
        # Read in the message in the way of the bytes from the socket. ##
        # 4096 was chosen since it should be a power of 2 and documentation ##
        # said 4096 is recommended so ¯\_(ツ)_/¯ ##
        message = connection_socket.recv(4096).decode()
        print("Connection socket receives")

        if not message:
            connection_socket.close()
            print("Close connection socket if message not received, break out\n")
            break

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1]

        # Because the extracted path of the HTTP request includes
        # a character '\', we read the path from the second character
        x = 0
        for file_in_cache in os.listdir(folder_path):
            if file_in_cache == filename[1:]:
                print("File found in cache\n")
                f = open(filename[1:], "rb")
                output_data = f.read()
                connection_socket.send("HTTP/1.1 200 OK \r\n\r\n".encode())
                connection_socket.send(output_data)
                connection_socket.send("\r\n".encode())
                connection_socket.close()
                f.close()
                print("File sent through connection socket and socket closed\n")
                x = 1
                break
        if x == 1:
            continue

        split_string = filename.split('/')
        hostname = split_string[1].split(':')
        serverPort = hostname[1]
        host = hostname[0]
        # create TCP socket on client to use for connecting to remote server.
        clientSocket = socket(AF_INET, SOCK_STREAM)
        print("Client socket created\n")
        # open the TCP connection
        clientSocket.connect((host, int(serverPort)))
        print("Client socket connected\n")
        # interactively get user's line to be converted to upper case
        clientSocket.send(message.encode())
        print("Client socket sends message, encoded")
        # get user's line back from server having been modified by the server
        file_data = ""
        from_server = ""
        while from_server != "":
            from_server = clientSocket.recv(4096).decode()
            file_data += from_server

        with open(os.path.join(folder_path, split_string[2]), "wb") as out_file:
            out_file.write(file_data.encode())

        f = open(split_string[2], "rb")
        # Store the entire content of the requested file in a temporary
        # buffer
        output_data = f.read()
        f.close()
        # Send the HTTP response header line to the connection socket
        connection_socket.send("HTTP/1.1 200 OK \r\n\r\n".encode())

        # Send the content of the requested file to connection socket
        # for i in range(0, len(outputdata)):
        connection_socket.send(output_data)
        connection_socket.send("\r\n".encode())

        # Close the client connection socket
        connection_socket.close()

    except IOError:
        # Send HTTP response message for file not found
        # Fill in start
        connection_socket.send("404 Not Found\n".encode())

        # Close the client connection socket
        connection_socket.close()

proxy_socket.close()
