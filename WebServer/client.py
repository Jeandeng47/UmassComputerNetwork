from socket import *
import sys

def start_client(host, port, file_name):
    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # prepare and send request
        request = (
            "GET /" + file_name + " HTTP/1.1\r\n"
            "Host: " + host + "\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        client_socket.send(request.encode())
        print(f"Sent request for {file_name}")

        # receive response
        response = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk
        print("Received response from server.")

    finally:
        client_socket.close()
        print("Connection closed.")
   

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 client.py <server_host> <sever_port> <file_name>") 
        sys.exit(1)
        
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
        file_name = sys.argv[3]
    except ValueError:
        print("Port number must be an integer.")
        sys.exit(1)

    start_client(host, port, file_name)
