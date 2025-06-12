# Single Threaded Server
from socket import *
import sys

def run_server(port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # reuse address
    server_socket.bind(('', port))
    server_socket.listen(1) # keep at most 1 connection in queue
    print(f"Server is running on port {port}...")

    while True:
        try:
            # accept connection
            conn, addr = server_socket.accept()
            print(f"Connection established with {addr}")

            # receive data
            request = conn.recv(1024).decode()
            print(f"Received data: {request}")

            # parse data and read
            # e.g. GET /HelloWolrd HTTP/1.1
            parts = request.split()
            if len(parts) < 2:
                raise IOError("Invalid request format")
            filename = parts[1]
            with open(filename[1:], 'r') as file: # remove leading '/'
                data = file.read()
            print(f"Finished reading file: {filename[1:]}")

            # sned HTTP header and data
            header = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "\r\n"
            )
            conn.send(header.encode())
            
            for line in data.splitlines():
                conn.send((line + "\r\n").encode())
            print("Data sent successfully.")
            
            # close connection
            conn.close()
            print(f"Connection with {addr} closed.")

        except IOError:
            # File not found
            error_resp = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                "\r\n"
                "<html><body><h1>404 Not Found</h1></body></html>\r\n"
            )
            conn.send(error_resp.encode())
            conn.close()
            print("File not found, sent 404 response.")

    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <port_number>")
        sys.exit(1)
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Port number must be an integer.")
        sys.exit(1)
    run_server(port)