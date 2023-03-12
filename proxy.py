# Import socket module
from socket import *
import os

# Set the path of the folder you want to create
folder_path = 'cache_folder'

# Create the folder if it does not exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Establish the socket, bind it to the port and let it listen for connections
proxy_socket = socket(AF_INET, SOCK_STREAM)
proxy_socket.bind(("", 8888))
proxy_socket.listen(1)
while True:
    print('Ready to serve...')
    # Accept the connection from the proxy socket
    connection_socket, addr = proxy_socket.accept()
    try:
        message = connection_socket.recv(4096).decode()
        # Extract the filename, the hostname, and the server port
        filename = message.split()[1]
        split_string = filename.split('/')
        hostname = split_string[1].split(':')
        serverPort = hostname[1]
        host = hostname[0]

        # Check if the file is in the cache folder. If there, send it from there
        loop_check = 0
        for file_in_cache in os.listdir(folder_path):
            file_discovery = file_in_cache.split("-")
            if  file_discovery[1] == split_string[2] and \
                file_discovery[0] == serverPort:
                f = open(os.path.join(folder_path, file_in_cache), "rb")
                output_data = f.read()
                if "HTTP/1.1 404" in output_data.decode():
                    print("Hello")
                    break
                connection_socket.send("HTTP/1.1 200 OK \r\n\r\n".encode())
                connection_socket.send(output_data)
                #connection_socket.send("\r\n".encode())
                connection_socket.close()
                f.close()
                loop_check = 1
                break
        if loop_check == 1:
            continue

        # create TCP socket on client to use for connecting to remote server.
        clientSocket = socket(AF_INET, SOCK_STREAM)
        # open the TCP connection
        clientSocket.connect((host, int(serverPort)))
        send_message = "GET " + "/" + split_string[2] + " HTTP/1.1"
        # interactively get user's line to be converted to upper case
        clientSocket.send(send_message.encode())
        # get user's line back from server having been modified by the server
        from_server = clientSocket.recv(4096)
        data = from_server.decode()
        # If the header is there in the message received, then remove it
        # from the file
        if "HTTP/1.1 200 OK" in data:
            from_server = from_server.replace(b"HTTP/1.1 200 OK \r\n\r\n", b'')
        # If the message received has 404, then the file wasn't found and we
        # send back the same message
        #elif "HTTP/1.1 404" in data:
         #   connection_socket.send("HTTP/1.1 404 Not Found \r\n\r\n".encode())
          #  connection_socket.close()
           # clientSocket.close()
            #continue
        print("Below HTTP Check\n")
        # Read till all data has been extracted
        file_data = from_server
        transfer_check = True
        while transfer_check:
            from_server = clientSocket.recv(4096)
            if from_server == b'':
                transfer_check = False
            else:
                file_data += from_server

        # Close the socket


        # Open and write the data to the file
        file_entry = serverPort + "-" + split_string[2]
        with open(os.path.join(folder_path, file_entry), "wb") as out_file:
            out_file.write(file_data)

        # Send back the data from the file to the socket
        if "HTTP/1.1 404 Not Found".encode() in file_data:
            # connection_socket.send("HTTP/1.1 404 Not Found\n".encode())
            print(file_data.decode())
            connection_socket.send(file_data)
        else:
            connection_socket.send("HTTP/1.1 200 OK \r\n\r\n".encode())
            connection_socket.send(file_data)
            # connection_socket.send("\r\n".encode())
        # Close the client connection socket
        connection_socket.close()
        clientSocket.close()
    except IOError:
        # Send HTTP response message for file not found
        connection_socket.send("HTTP/1.1 404 Not Found\n".encode())
        # Close the client connection socket
        connection_socket.close()


proxy_socket.close()
