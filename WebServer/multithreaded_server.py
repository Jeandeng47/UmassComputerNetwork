from socket import *
import sys
import threading

def handle_client(connection, addr):
    try:
        # handle request
        request = connection.recv(1024).decode()
        print(f"[{addr}]: {request.splitlines()[0]}")

        parts = request.split()
        if len(parts) < 2: raise IOError("Invalid request line")

        
        # read data from file
        # e.g. GET /index.html HTTP/1.1
        file_name = parts[1][1:]  # remove leading '/'
        with open(file_name, 'r') as f:
            data = f.read()
        print(f"Read data from file {file_name}")

        # send response
        header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
        )
        connection.send(header.encode())
            
        for line in data.splitlines():
            connection.send((line + "\r\n").encode())
        print("Data sent successfully.")

    except IOError:
        error = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<html><body><h1>404 Not Found</h1></body></html>\r\n"
        )
        connection.send(error.encode())
    finally:
        connection.close()
        print(f"[{addr}] connection closed")


def run_server(port):
    # set up a main thread
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(10) # allow up to 10 connections

    while True:
        connection, addr = server_socket.accept()
        print(f"Accepted connection from addr {addr}...")

        # start a new thread for each client
        # daemon=True, this thread run in background
        # the program will not wait for them and exits
        t = threading.Thread(target=handle_client, args=(connection, addr), daemon=True)
        t.start()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 multithreaded_server.py <server_port>")
    try: 
        port = int(sys.argv[1])
    except ValueError:
        print("Port number must be an integer.")
        sys.exit(1)
    run_server(port)
    