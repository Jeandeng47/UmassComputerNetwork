# Lab05: Simple HTTP Proxy Server with Caching

This is a minimal HTTP proxy server designed for lab exercises. It supports forwarding HTTP GET requests and caching responses locally.

## Features:
- HTTP GET Proxying: Forwards HTTP/1.0 and HTTP/1.1 GET requests to origin servers.

- Local Caching: Stores fetched responses under `./<host>/<path>`. Subsequent requests for the same resource are served from cache, reducing latency.

## Requirements

- Python 3.6 or higher

## Usage

1. Navigate to the project directory `Webproxy`

2. Start the proxy server:
    ```bash
    python3 proxy_server.py <SERVER_IP> [PORT]
    ```

    - `SERVER_IP`: IP address to bind the proxy (e.g., 127.0.0.1).

    - `PORT`: Optional port number.

3. Configure your HTTP client to use the proxy:
    - curl 

        ```bash
        curl -v -x <SERVER_IP>:<PORT> http://example.com/
        ```
    - Browser: Set the HTTP proxy address to `<SERVER_IP>:<PORT>` in network preferences.

4. Access any HTTP URL through the proxy.