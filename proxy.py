# Import socket module
from socket import *    

# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

server_socket = socket(AF_INET, SOCK_STREAM)

# Fill in start

# Establish the port to be bound to and bind it to the server_socket #
server_socket.bind(('', 6789))
# Start listening to allow socket to accept connection requests, 1 so that #
# it handles only one request at a time #
server_socket.listen(1)

# Fill in end 

# Server should be up and running and listening to the incoming connections
while True:
    print('Ready to serve...')
    # Set up a new connection from the client
    # Fill in start

    # Accepts the connection being "listened" from the server socket ##
    connection_socket, addr = server_socket.accept()

    # Fill in end

    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except clause is executed
    try:
        # Receives the request message from the client
        # Fill in start

        # Read in the message in the way of the bytes from the socket. ##
        # 4096 was chosen since it should be a power of 2 and documentation ##
        # said 4096 is recommended so ¯\_(ツ)_/¯ ##
        message = connection_socket.recv(4096).decode()

        if not message:
            connection_socket.close()
            break
        # Fill in end

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1]

        # Because the extracted path of the HTTP request includes
        # a character '\', we read the path from the second character
        f = open(filename[1:])

        # Store the entire content of the requested file in a temporary
        # buffer
        outputdata = f.read()  # Fill in start         #Fill in end
        f.close()

        # Send the HTTP response header line to the connection socket

        # Fill in start

        connection_socket.send("HTTP/1.1 200 OK \r\n\r\n".encode())
        # Fill in end
 
        # Send the content of the requested file to connection socket
        for i in range(0, len(outputdata)):
            connection_socket.send(outputdata[i].encode())
        connection_socket.send("\r\n".encode())

        # Close the client connection socket
        connection_socket.close()

    except IOError:
        # Send HTTP response message for file not found
        # Fill in start

        connection_socket.send("404 Not Found\n".encode())

        # Close the client connection socket
        connection_socket.close()

server_socket.close()

