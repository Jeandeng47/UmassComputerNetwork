import random
from socket import *

# create a UDP socket
server_socket = socket(AF_INET, SOCK_DGRAM)
# assign ip and port
server_socket.bind(('', 12000))

while True:
    # Generate artifical packet loss
    rand = random.randint(0, 10)
    msg, addr = server_socket.recvfrom(1024)
    msg = msg.upper()
    # consider 40% random packer loss
    if rand < 4:
        continue
    server_socket.sendto(msg, addr)
