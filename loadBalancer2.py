import socket

#Define o IP adress e ports dos servidores
servers = [('192.168.1.81', 5555), ('192.168.1.81', 5656)]

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('0.0.0.0', 80))
listen_socket.listen(25)

#Inicia o indice dos servidores a 0
current_servers = 0

while True:
    #Wait for a client to connect
    client_connection, client_address = listen_socket.accept()
    print(f'[*] Accepted connection from address: {client_address[0]}:{client_address[1]}')
    request = listen_socket.recv(4096)

    try:
        #Escolhe os servidores com o round robin
        server_address = servers[current_servers]
        current_servers = (current_servers + 1) % len(servers)

        #conecta ao servidor escolhido e envia o pedido
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(server_address)
        
        server_socket.sendall(request)

        #Recebe a resposta do servidor e envia para o cliente
        while True:
            data = server_socket.recv(1024)
            if not data:
                break
            client_connection.sendall(data)
    finally:
        client_connection.close()
        server_socket.close()