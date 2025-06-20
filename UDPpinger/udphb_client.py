from socket import *
import struct
import time

host = 'localhost'
port = 13000

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)

seq_num = 0
interval = 1

try:
    while True:
        t_stamp = time.time()
        msg = struct.pack('!I d', seq_num, t_stamp)

        client_socket.sendto(msg, (host, port))
        print(f"Sent heartbeat: seq = {seq_num}, timestamp = {t_stamp}")
        
        seq_num += 1
        time.sleep(interval)
except KeyboardInterrupt:
    print("Heartbeat client stopped by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client_socket.close()
    print("Heartbeat client stopped.")
