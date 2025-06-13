# Lab 1: Python Web Server & Minimal HTTP Client

A lightweight HTTP/1.1 web server (single-threaded and multithreaded variants) and a matching command-line HTTP client in Python. This lab illustrates basic TCP socket programming, HTTP message formats, and concurrent request handling.

---

## Overview

- **Single-Threaded Server (`server.py`)**  
  - Listens on a user-specified TCP port  
  - Handles one client at a time (no concurrency)  
  - Serves static `.html` files from the working directory  
  - Returns `200 OK` with `Content-Type: text/html` for existing files  
  - Returns `404 Not Found` for missing files (including `/favicon.ico`)  
  - Logs each request and response status to the console  

- **Multithreaded Server (`server_threaded.py`)**  
  - Listens on a user-specified TCP port  
  - Spawns a new thread for each connection to handle multiple clients concurrently  
  - Same request/response behavior as the single-threaded server  

- **HTTP Client (`client.py`)**  
  - Connects to a server over TCP  
  - Sends an HTTP `GET` request for a specified file  
  - Displays the raw HTTP response (headers + body)  

---

## Requirements

- Python 3.x  
- ApacheBench 2.x

---

## Installation

1. **Clone or download** this project directory to your local machine.  
2. **Verify Python 3** is installed:  
   ```bash
   python3 --version
   ```  
3. (optional) Verify ApacheBench is installed:
   ```bash
   ab -V
   ```  

---

## Usage

### 1. Single-Threaded Server (`server.py`)

1. Open a terminal in this directory.  
2. Run:  
   ```bash
   python3 server.py <port>
   ```  
   Example:  
   ```bash
   python3 server.py 6789
   ```  
3. The console will display:  
   ```
   Server is listening on port 6789...
   ```  
4. Stop the server with `Ctrl+C`.

### 2. HTTP Client (`client.py`)

1. Open a new terminal in this directory.  
2. Run:  
   ```bash
   python3 client.py <host> <port> <filename>
   ```  
   Example:  
   ```bash
   python3 client.py localhost 6789 HelloWorld.html
   ```  
3. The raw HTTP response (headers and HTML) will be printed to your console.

### 3. Multithreaded Server (`server_threaded.py`)

1. Open a terminal in this directory.  
2. Run:  
   ```bash
   python3 server_threaded.py <port>
   ```  
   Example:  
   ```bash
   python3 server_threaded.py 6789
   ```  
3. The console will display:  
   ```
   Multithreaded server listening on port 6789...
   ```  
4. Stop with `Ctrl+C`. 

### 4. Methods to Request

- **Browser:** navigate to  
  ```
  http://localhost:<port>/HelloWorld.html
  ```  
- **curl:**  
  ```bash
  curl http://localhost:<port>/HelloWorld.html
  ```
- **ApacheBench**: for concurrency test
  ```bash
  ab -n <num_of_requests> -c <concurrency_level> http://localhost:<port>/HelloWorld.html
  ```
---

## ⚠️ Notes

- Servers use plain HTTP (no TLS/HTTPS).  
- Only the `GET` method is supported.  
- `server.py` is single-threaded; `server_threaded.py` supports concurrency.

---

## 📄 License

This project is provided for educational purposes only.
