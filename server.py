import socket
import ssl
import threading

class ProxyServer:
    def _init_(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Proxy server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket):
        request_data = client_socket.recv(4096)
        print("Received request:")
        print(request_data.decode())

        # Extracting the hostname from the request
        hostname = self.extract_hostname(request_data.decode())

        try:
            remote_socket = socket.create_connection((hostname, 443))
            ssl_socket = ssl.wrap_socket(remote_socket)

            ssl_socket.sendall(request_data)
            response_data = ssl_socket.recv(4096)
            print("Received response:")
            print(response_data.decode())

            client_socket.sendall(response_data)
        except Exception as e:
            print("Error:", e)

        client_socket.close()

    def extract_hostname(self, request):
        lines = request.split("\n")
        host_line = next(line for line in lines if line.startswith("Host:"))
        return host_line.split(" ")[1].strip()

    def start(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "_main_":
    proxy = ProxyServer('127.0.0.1', 8888)
    proxy.start()
