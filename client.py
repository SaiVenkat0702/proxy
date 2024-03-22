import socket

def send_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 8888))
        client_socket.sendall(request.encode())
        response = client_socket.recv(4096)
        print("Received response from proxy:")
        print(response.decode())

if __name__ == "_main_":
    # Example HTTP request
    http_request = "GET http://example.com HTTP/1.1\r\nHost: example.com\r\n\r\n"
    send_request(http_request)

    # Example HTTPS request
    https_request = "GET https://www.example.com HTTP/1.1\r\nHost: www.example.com\r\n\r\n"
    send_request(https_request)