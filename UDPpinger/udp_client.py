from socket import *
import time

def send_ping():
    dest_ip = 'localhost'
    dest_port = 12000
    count = 10
    timeout_sec= 1

    # no connect()
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(timeout_sec)

    rtts = []
    losses = 0

    # send 10 pings
    for i in range(count):
        try:
            send_t = time.time()
            msg = f"Ping {i + 1} {send_t}" # seq_num starts at 1
            
            client_socket.sendto(msg.encode(), (dest_ip, dest_port))
            data, addr = client_socket.recvfrom(1024)
            recv_t = time.time()
            rtt = (recv_t - send_t) * 1000 # milisec
            rtts.append(rtt)

            print(f"PING {i+1}: Reply = {data.decode()}, time = {rtt:.2f} ms")
        except timeout:
            print(f"PING {i+1}: Request timed out.")
            losses += 1

        time.sleep(1)

    client_socket.close()

    print("\n--- Ping statistics ---")
    print(f"Total pings = {count},{100 * losses / count: .0f}% packets losses")
    if rtts:
        print(f"rtt Avg: {sum(rtts) / len(rtts): .2f}")    
        print(f"rtt Min: {min(rtts): .2f}")    
        print(f"rtt Max: {max(rtts): .2f}")    
    
if __name__ == "__main__":
    send_ping()
