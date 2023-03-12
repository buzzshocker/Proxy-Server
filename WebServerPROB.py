# Import socket module
from socket import *

# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

# Establish the server socket
server_socket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to a port and start listening
server_socket.bind(("", 6789))
server_socket.listen(1)

while True:
    print('Ready to serve...')
    # Assign connection socket to the server socket
    connection_socket, addr = server_socket.accept()

    try:
        message = connection_socket.recv(4096).decode()

        if "HTTP/1.1 404" in message:
            connection_socket.send("HTTP/1.1 404 Not Found \r\n\r\n")
            connection_socket.close()
            continue

        filename = message.split()[1]
        f = open(filename[1:], "rb")
        output_data = f.read()
        f.close()

        connection_socket.send("HTTP/1.1 200 OK \r\n\r\n".encode())
        connection_socket.send(output_data)
        # Close the client connection socket
        connection_socket.close()

    except IOError:
        # Send HTTP response message for file not found
        connection_socket.send("404 Not Found\n".encode())
        # Close the client connection socket
        connection_socket.close()

server_socket.close()

