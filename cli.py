import socket
import tcp
from signal import signal, SIGINT
from sys import exit
from operator import itemgetter
import time

"""
    start and dest: (ip, port)
    assume initial window size 5840 byte
    assume initial packet size 1400 byte
"""

'''
    initialize the first packet to be sent
    start and dest are tuples (addr, port)
'''
def pack_init(from_port, to_port, seq, ack, off, bit, wdw, msg):
    pack = tcp.Tcp_pack()
    pack.set_ports(from_port, to_port)# from port to port
    pack.set_seq_num(seq)
    pack.set_ack_num(ack)
    pack.set_misc(off, bit) # data offset unknown yet, so bit set later
    pack.set_wdw_size(wdw)
    pack.set_msg(msg)
    pack.check_sum_16bit()
    return pack
    

'''
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
'''

def estm_rtt_update(smpl_rtt, estm_rtt):
    ALPHA = 1/8
    return (1-ALPHA) * estm_rtt + ALPHA*smpl_rtt


'''Functions for finding a packet from list'''

# find pack by seq number in list of packets
def search_by_seq(ls, seq):
    res = [item for item in ls if item[0] == seq]
    if len(res != 1):
        print("packet repeat error.")
    else:
        return res[0]

def check_timeout(ls):
    
    t_curr = time.time()
    for pack in on_the_fly_list:
        t_prev = 
        

    # if estab: send back estab
'''constantly send and recv a file until ctrl_c'''
def send_data_cli(start_port, dest_port, sock, udp_dest, msg):
    loco_seq = 111
    remo_acked = 998  # assume we start to transform after 998 is acked
    
    MSS = 1500 # max segment window
    wdw_remo = 1*MSS # init to one will change gradually
    wdw_loco = 1*MSS # init to one controlled by remote device
    on_the_fly = [] # packet that are sent but not acked (seq, pack, timestamp)
    recv_un_use = [] # packet that are recved but not consumed by app (seq, pack)
    
    # var for rtt calc
    t_prev = time.time() # time stamp for previous packet
    estm_rtt = 1 # estimated rtt
    
    # var for slow start
    cwnd = 1 * MSS
    t_cwnd_prev_upd = time.time() # time of last window change
    ssthresh = 64000 # additive inc thresh
    ack_repeat = 0 #number of ack repeat
    
    while True: # general kill switch
        '''Try to recv new packets'''
        while len(recv_un_use) < wdw_loco: # keep receiving until local buffer filled
            try:
                recv_pack =tcp.Tcp_pack()
                recv_pack.recv_pack(sock)
                t_curr = time.time() # record recv time
                recv_un_use.append((recv_pack.get_seq_num(), recv_pack, t_curr)) # store recv pack and its time
                #TODO: handle vars: recv success
                
                #1 handle rtt
                try:
                    t_prev = search_by_seq(on_the_fly, recv_pack.get_ack_num())[2] # get the time pack was sent
                    smpl_rtt = t_curr-t_prev
                    estm_rtt = estm_rtt_update(smpl_rtt, estm_rtt)
                except (KeyError,ValueError) as e: # got an ack with no record
                    print("got error {}.".format(e))
                t_prev = t_curr
                
                #2 handle cwnd
                if recv_pack.get_ack_num() == loco_seq: # ack an acked seq #
                    ack_repeat += 1
                    if ack_repeat >= 3: # pack lost resend
                        cwnd = cwnd/2
                        ack_repeat = 0
                    
                if t_curr-t_cwnd_prev_upd > estm_rtt:
                    if cwnd > ssthresh: # additive inc
                        cwnd += 1 
                    else:
                        cwnd = cwnd * 2 # expo inc
                    t_cwnd_prev_upd = t_curr
                
            except:
                # no recv, do nothing
                break
            
        '''Check for timeouts'''
            
        
        '''Try to send out packets'''
        # keep sending until cwnd reached
        while len(on_the_fly) < wdw_remo:
            try:
                # prepare pack_to_send
                pack_to_send = pack_init (start_port, dest_port, loco_seq, remo_acked, 5, 0x02, wdw_remo, msg) # first pack: ack 998, seq 111
                pack_to_send.send_pack(sock, udp_dest)                
                on_the_fly.append((time.time(), pack_to_send)) 
                #TODO: handle vars: send success
            except:
                #TODO: handle vars: send failed
                break


    '''
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
        pack.send_pack(sock, udp_dest)
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
    '''


'''exception handlers'''          
def sigint_handler(signum, frame):
    # Handle any cleanup here
    print('{} detected in {}. Exiting gracefully'.format(signum, frame))
    exit(0)

def sock_no_read_handler():
    pass


'''main function'''
def main():
    # initial setup
    signal(SIGINT, sigint_handler)
    send_to = ("127.0.0.1", 20003)
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.setblocking(0)
    # communication begin
    send_data()
    


if __name__ == "__main__":
    main()

 
   

   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
            