# Import socket module
from socket import *    

# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

server_socket = socket(AF_INET, SOCK_STREAM)

# Establish the port to be bound to and bind it to the server_socket #
server_socket.bind(("", 6789))
# Start listening to allow socket to accept connection requests, 1 so that #
# it handles only one request at a time #
server_socket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
    print('Ready to serve...')
    # Set up a new connection from the client
    # Fill in start

    # Accepts the connection being "listened" from the server socket ##
    connection_socket, addr = server_socket.accept()

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
        print("Message", message)

        if not message:
            connection_socket.close()
            break

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1]
        print(filename)

        # Because the extracted path of the HTTP request includes
        # a character '\', we read the path from the second character
        f = open(filename[1:], "rb")

        # Store the entire content of the requested file in a temporary
        # buffer
        output_data = f.read()
        f.close()

        # Send the HTTP response header line to the connection socket

        connection_socket.send("HTTP/1.1 200 OK \r\n\r\n".encode())
 
        # Send the content of the requested file to connection socket
        # for i in range(0, len(outputdata)):
        connection_socket.send(output_data)
        # connection_socket.send("\r\n".encode())

        # Close the client connection socket
        connection_socket.close()

    except IOError:
        # Send HTTP response message for file not found
        connection_socket.send("404 Not Found\n".encode())
        # Close the client connection socket
        connection_socket.close()

server_socket.close()


