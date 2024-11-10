import socket

HOST = '192.168.1.81'
PORT = 8080

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
sock.bind((HOST, PORT))

# Listen for incoming connections
sock.listen(5)

while True:
    # Accept an incoming connection
    client_sock, client_addr = sock.accept()
    print("Received connection from", client_addr)

    # Choose a server to forward the connection to
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect(('192.168.1.81', 5555))

    # Forward the connection
    server_sock.sendall(client_sock.recv(1024))

    # Close the connections
    client_sock.close()
    server_sock.close()