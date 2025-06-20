# Lab2: UDP Messaging and Heartbeat System

This project contains two UDP-based systems implemented in Python:

1. **Basic UDP Messaging** — Sends a single message from client to server.
2. **UDP Heartbeat System** — Periodically sends heartbeat packets from client to server with sequence numbers and timestamps. The server detects packet loss and client inactivity.

## 1. Basic UDP Messaging

### udp_server.py

- Binds to a specified UDP port (default: 12000)
- Receives and prints a single message

### udp_client.py

- Sends a string message to the server at a specified address and port

### How to Run

Terminal 1:
```
python3 udp_server.py
```

Terminal 2:
```
python3 udp_client.py
```

## 2. UDP Heartbeat System

### udphb_client.py

- Sends UDP packets every second to a server
- Each packet contains:
  - An integer sequence number
  - A float timestamp (Unix time)
- Uses `struct.pack('!I d', ...)` to format data in network byte order

### udphb_server.py

- Receives and unpacks the heartbeat packets
- Validates packet order and detects:
  - Lost packets (based on skipped sequence numbers)
  - Client inactivity (no packet received within 5 seconds)
- Uses `socket.settimeout()` to periodically check for timeout

### How to Run

Terminal 1:
```
python3 udphb_server.py
```

Terminal 2:
```
python3 udphb_client.py
```

## Requirements

- Python 3.x
- Standard libraries only: `socket`, `struct`, `time`

