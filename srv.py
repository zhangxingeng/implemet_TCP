import socket
import tcp
from signal import signal, SIGINT
from sys import exit


def srv_listen(sock):
    recv = tcp.Tcp_pack()
    cli_bind = recv.recv_pack(sock)
    recv.print_pack()
    recv.set_ack_num(recv.get_seq_num()+1) # use same seq number as sender
    recv.set_misc(5, 0x12)
    recv.send_pack(sock, cli_bind)
    
    
def srv_respond(sock):
    seq_num_loco = 1000
    ack_remo = 0
    recv = tcp.Tcp_pack()
    i = 0
    while True:
        cli_bind = recv.recv_pack(sock)
        print("got in: ack# {} seq# {}".format(recv.get_ack_num(), recv.get_seq_num()))
        # check for ack from the other side
        if recv.get_ack_num() == 0:
            recv.set_seq_num(1000)
            ack_remo += 1
            recv.set_ack_num(ack_remo)
        elif recv.get_ack_num() > seq_num_loco: # initial ack aggreed on handshake
            ack_remo = recv.get_seq_num()+1
            recv.set_ack_num(ack_remo)
            seq_num_loco += 1
            recv.set_seq_num(seq_num_loco) # initial seq on this side
        else:
            print("got an error")
            exit()
        recv.set_misc(5, 0x12)
        recv.set_msg("Hello Client")
        print("send out: ack# {} seq# {}".format(recv.get_ack_num(), recv.get_seq_num()))
        recv.send_pack(sock, cli_bind)
        i = i+1
    
    #recv from cli
    # if estab: estabbed

def handler(signum, frame):
    # Handle any cleanup here
    print('{} detected in {}. Exiting gracefully'.format(signum, frame))
    exit(0)
    
    
signal(SIGINT, handler)
# Create a socket
local_addr_port   = ("127.0.0.1", 20003)
udp_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_sock.bind(local_addr_port)
print("UDP server up and listening")

srv_respond(udp_sock)
    
    
    
    
    
    
    
    
