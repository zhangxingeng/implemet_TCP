import socket
import tcp

def srv_listen(sock):
    recv = tcp.Tcp_pack()
    cli_bind = recv.recv_pack(sock)
    recv.print_pack()
    recv.set_ack_num(recv.get_seq_num()+1) # use same seq number as sender
    recv.set_misc(5, 0x12)
    recv.send_pack(sock, cli_bind)
    
    #recv from cli
    # if estab: estabbed


# Create a socket
local_addr_port   = ("127.0.0.1", 20002)
udp_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_sock.bind(local_addr_port)
print("UDP server up and listening")


while(True):
    srv_listen(udp_sock)
    
    
    
    
    
    
    
    
