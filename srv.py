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






def send_data_srv(start_port, dest_port, sock, udp_dest, msg):
    loco_seq = 999
    remo_acked = 110    # assume we start to transform after 110 is acked
    wdw_remo = 100
    
    # recv remote pack seq 111, ack it check ack for loco pack
    
    pack_init (start_port, dest_port, loco_seq, remo_acked, 5, 0x02, wdw_remo, msg) # 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def srv_respond(sock):
    seq_num_loco = 1000 # keep record of local packet sequence number
    ack_remo = 0 # keep record of ack for remote packets
    recv = tcp.Tcp_pack()
    i = 0
    
    recv_winodw = [] # store packet received seq number (append when recv, remove from top when insequence)
    recv_valid = 0
    send_window = [] # keep record of on the fly packets
    send_valid = 1000
    ertt = 0.1 # estimated rtt
    drtt = 0.1 # deviance of rtt
    
    while True:
        cli_bind = recv.recv_pack(sock)     # recv a packet
        recv_winodw.append(recv.get_seq_num())  # append to recv window

        if recv.get_ack_num() == 0:     # update ack and seq number
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
        send_window.append(recv.get_seq_num)
        i = i+1
    
    #recv from cli
    # if estab: estabbed

def sigint_handler(signum, frame):
    # Handle any cleanup here
    print('{} detected in {}. Exiting gracefully'.format(signum, frame))
    exit(0)
    
    
signal(SIGINT, sigint_handler)
# Create a socket
local_addr_port   = ("127.0.0.1", 20003)
udp_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_sock.bind(local_addr_port)
print("UDP server up and listening")

srv_respond(udp_sock)
    
    
    
    
    
    
    
    
