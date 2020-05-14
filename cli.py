import socket

import numpy as np

'''
# Create a UDP socket
srv_addr_port   = ("127.0.0.1", 20001)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# send msg
UDPClientSocket.sendto(str.encode("Hello UDP Server"), srv_addr_port)
# recv msg
recv_msg = UDPClientSocket.recvfrom(1024)
print("Message from Server {}".format(recv_msg[0]))
'''





class Tcp_pack:
    def __init__(self, pack_hd):
            self.src_port = np.uint16(pack_hd[0]) # 16 bit
            self.dest_port = np.uint16(pack_hd[1]) # 16 bit
            self.seq_num = np.uint32(pack_hd[2]) # 32 bit
            self.ack_num = np.uint32(pack_hd[3]) # 32 bit
            self.misc = np.uint16(pack_hd[4]) # 16 bit for header len and flags
            self.wdw_size = np.uint16(pack_hd[5]) # 16 bit
            self.ck_sum = np.uint16(pack_hd[6]) # 16 bit calc afterwards
    
    def set_src_port(self, src_port):
        self.src_port = np.uint16(src_port)   
    def get_src_port(self):
        return self.src_port
   
    def set_dest_port(self, dest_port):
        self.dest_port = np.uint16(dest_port)
    def get_dest_port(self):
        return self.dest_port
    
    def set_seq_num(self, seq_num):
        self.seq_num = np.uint32(seq_num)
    def get_seq_num(self):
        return self.seq_num
    
    def set_ack_num(self, ack_num):
        self.ack_num = np.uint32(ack_num)
    def get_ack_num(self):
        return self.ack_num
    
    def set_misc(self, misc):
        self.misc = np.uint16(misc)
    def get_misc(self):
        return self.misc
    
    def set_wdw_size(self, wdw_size):
        self.wdw_size = np.uint16(wdw_size)
    def get_wdw_size(self):
        return self.wdw_size
    
    def set_ck_sum(self, ck_sum):
        self.ck_sum = np.uint16(ck_sum)
    def get_ck_sum(self):
        return self.ck_sum        
    
    def send_pack(self, sock, send_to):
        send_msg = self.src_port+':'+self.dest_port+':'+ \
              self.seq_num+':'+self.ack_num+':'+ \
              self.misc+':'+self.wdw_size+':'+self.ck_sum
        sock.sendto(str.encode(send_msg), send_to)         
        
    def recv_pack(self, sock):
        recv_msg = sock.recvfrom(1024)
        tokens = recv_msg.split(':')
        return Tcp_pack(tokens)
        
                
def iptoint(ip):
    return np.uint32(socket.inet_aton(ip).encode('hex'),16)

def inttoip(ip):
    return socket.inet_ntoa(hex(ip)[2:].decode('hex'))


src_p = 36869
des_p = 23
seq_n = 1913975060
ack_n = 0
dat_off = 6 # in words, 4*8bit
flg = 0x02 # syn
wdw = 8760
cksum = 0xa92c
misc = np.uint16("{0:04b}000{1:09b}".format(dat_off, flg))
b = '{0:x}:{1:x}:{2:x}:{3:x}:{4:x}:{5:x}:{6:x}'.format(src_p, des_p, seq_n, ack_n, misc, wdw, cksum)
c = [int(v,16) for v in b.split(':')]
pack = Tcp_pack(c)
print("input checksum: {}; output: {}".format(cksum, pack.get_ck_sum()))
            
            
            
            
            
            