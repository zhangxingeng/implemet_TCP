import socket
import tcp
from signal import signal, SIGINT
from sys import exit
import time

"""
    start and dest: (ip, port)
    assume initial window size 5840 byte
    assume initial packet size 1400 byte
"""

def cli_listen(start, dest, sock, send_to):
    to_send = tcp.Tcp_pack()
    to_send.set_ports(start[1], dest[1])# from port to port
    to_send.set_seq_num(0)
    to_send.set_ack_num(0)
    to_send.set_misc(5, 0x02) # data offset unknown yet, so bit set later
    to_send.set_wdw_size(5840)
    to_send.check_sum_16bit()
    print("-----pack to send------")
    to_send.print_pack()
    to_send.send_pack(sock, send_to)
    to_send.recv_pack(sock) # got syn from server
    print("-----Recved Pack-------")
    to_send.print_pack()
    
    # if estab: send back estab
'''constantly send and recv a file until ctrl_c'''
def send_data(start, dest, sock, send_to, msg):
    seq_num_loco = 0
    ack_remo = 1000
    # first packet init
    pack = tcp.Tcp_pack()
    pack.set_ports(start[1], dest[1])# from port to port
    pack.set_seq_num(seq_num_loco)
    pack.set_ack_num(0)
    pack.set_misc(5, 0x02) # data offset unknown yet, so bit set later
    pack.set_wdw_size(5840)
    pack.check_sum_16bit()
    i = 0
    
    # start sending packets
    while True:
        i = i+1
        pack.set_msg(msg)
        start = time.time()
        print("send out: ack# {} seq# {}".format(pack.get_ack_num(), pack.get_seq_num()))
        pack.send_pack(sock, send_to)
        pack = tcp.Tcp_pack()
        pack.recv_pack(sock) # got syn from server
        print("got in: ack# {} seq# {}".format(pack.get_ack_num(), pack.get_seq_num()))
        end = time.time()
        # 
        if pack.get_ack_num() > seq_num_loco: # agreed server init seq
            ack_remo = pack.get_seq_num() + 1
            pack.set_ack_num(ack_remo)
            seq_num_loco += 1 
            pack.set_seq_num(seq_num_loco)
            
        else:
            print("Sorry packet was lost.")
            exit()
            
        # limit pack number
        #if i == 10:
           # break
    return
            
def handler(signum, frame):
    # Handle any cleanup here
    print('{} detected in {}. Exiting gracefully'.format(signum, frame))
    exit(0)
        

if __name__ == "__main__":
    signal(SIGINT, handler)
    
    
    send_to = ("127.0.0.1", 20003)
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    send_data(("127.0.0.1", 20001), ("127.0.0.1", 20002), sock, send_to, "Hello server!")


# constant send and recv msg
# apply control  
   

   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
            