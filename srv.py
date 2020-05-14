import socket

# Create a socket
local_addr_port   = ("127.0.0.1", 20001)
udp_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_sock.bind(local_addr_port)
print("UDP server up and listening")


while(True):
    # receive
    binder = udp_sock.recvfrom(1024)
    print("essage from Client:{}".format( binder[0]))
    print("Client IP Address:{}".format(binder[1]))
    # respond
    udp_sock.sendto(str.encode("Hello UDP Client"), binder[1])
    
    
    
    
    
    
    
    
