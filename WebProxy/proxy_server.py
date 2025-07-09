import os
import sys
from socket import *

DEFAULT_PORT = 7897
BUFFER_SIZE = 4096

def parse_args():
    if len(sys.argv) < 2:
        print("Usage: python proxy_server.py <server_ip> [port]")
        sys.exit(1)
    server_ip = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else DEFAULT_PORT
    return server_ip, port

def start_server(server_ip, port):
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_sock.bind((server_ip, port))
    server_sock.listen(5)
    print(f'Proxy server running on {server_ip}:{port}')
    return server_sock

def receive_request(client_sock):
    request = client_sock.recv(BUFFER_SIZE).decode()
    print('Request received:')
    print(request)
    return request 

def parse_request(request):
    parts = request.split()
    url = parts[1]
    if url.startswith('http://'):
        url = url[len('http://'):]
    host, _, path = url.partition('/')
    path = '/' + path
    print("host: " + host)
    print("path: " + path)
    return host, path

def get_from_cache(cache_file):
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            data = f.read()
        print(f'Cache hit: {cache_file}')
        return data
    else:
        print(f'Cache miss: {cache_file}')
        return None

def get_from_server(host, path):
    with socket(AF_INET, SOCK_STREAM) as remote_sock:
        print(f'Connect to the remote server: {host}')
        remote_sock.connect((host, 80))
        req_lines = [
            f"GET {path} HTTP/1.0",
            f"Host: {host}",
            "Connection: close",
            "",       
            "" 
        ]
        request = "\r\n".join(req_lines)
        print(">> Forwarding:\n", request)
        
        remote_sock.send(request.encode())
        response = b''
        while True:
            data_chunk = remote_sock.recv(BUFFER_SIZE)
            if not data_chunk:
                break
            response += data_chunk
    return response

def save_to_cache(cache_file, data):
    dir = os.path.dirname(cache_file)
    if dir and not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)
    with open(cache_file, 'wb') as f:
        f.write(data)
    print(f'Saved to cache: {cache_file}')
    
def send_response(client_sock, data):
    client_sock.sendall(data)
    print('Response sent to client.')

def handle_client(client_sock):
    request = receive_request(client_sock)
    host, path = parse_request(request)
    
    # build cache file
    cache_file = "." + os.sep + host + path.replace("/", os.sep)
    if path.endswith("/"):
        cache_file += "index.html"
    
    # try to get data from cache
    data = get_from_cache(cache_file)
    if data is None:
        try:
            data = get_from_server(host, path)
            save_to_cache(cache_file, data)
        except Exception as e:
            print('Error fetching from server:', e)
            not_found = b'HTTP/1.0 404 Not Found\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>'
            client_sock.sendall(not_found)
            client_sock.close()
            return
    send_response(client_sock, data)
    client_sock.close()

def main():
    server_ip, port = parse_args()
    server_sock = start_server(server_ip, port)
    try:
        while True:
            print('Waiting for client connection...')
            client_sock, addr = server_sock.accept()
            print(f'Client connected from {addr}')
            handle_client(client_sock)
    except KeyboardInterrupt:
        print('\nShutting down proxy server.')
    finally:
        server_sock.close()

if __name__ == '__main__':
    main()