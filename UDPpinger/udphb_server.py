from socket import *
import struct
import time

port = 13000
timeout_s = 5
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', port))
server_socket.settimeout(timeout_s)  # Set a timeout for receiving messages

print(f"Heartbeat server listening on port {port}...")

last_seq = -1
last_time = time.time()

try:
    while True:
        try:
            msg, addr = server_socket.recvfrom(1024)
            seq_num, t_stamp = struct.unpack('!I d', msg)

            current_time = time.time()
            if seq_num == last_seq + 1:
                print(f"Received heartbeat: seq = {seq_num}, timestamp = {t_stamp}")
                last_seq = seq_num
                last_time = current_time
            else:
                print(f"Out of order heartbeat: expected {last_seq + 1}, got {seq_num}")

        except timeout:
            if time.time() - last_time > timeout_s:
                print("No heartbeat received in the last 10 seconds. Server is inactive.")
                last_seq = -1  # Reset sequence number to indicate inactivity

        time.sleep(1)  # Sleep to avoid busy waiting
    
except KeyboardInterrupt:
    print("Heartbeat server stopped by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    server_socket.close()
    print("Heartbeat server stopped.")