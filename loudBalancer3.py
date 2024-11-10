import socket
import threading

class LoadBalancer:
    def __init__(self, host, port, servers):
        self.host = host
        self.port = port
        self.servers = servers
        self.server_index = 0
        self.server_lock = threading.Lock()

    def handle_client(self, client_socket):
        try:
            with self.server_lock:
                current_server = self.servers[self.server_index]
                self.server_index = (self.server_index + 1) % len(self.servers)

            # Encaminhe a conexão para o servidor atual
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect(current_server)
            data = client_socket.recv(4096)
            server_socket.send(data)
            
            # Adicione mais lógica conforme necessário

        except Exception as e:
            print(f"Error handling client connection: {e}")
        finally:
            client_socket.close()

    def start(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((self.host, self.port))
        listen_socket.listen(25)

        print(f"Load Balancer listening on {self.host}:{self.port}")

        while True:
            client_connection, _ = listen_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_connection,))
            client_handler.start()

if __name__ == "__main__":
    lb = LoadBalancer('0.0.0.0', 80, [('192.168.1.81', 5555), ('192.168.1.81', 5656)])
    lb.start()
