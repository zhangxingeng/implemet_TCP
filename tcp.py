import socket
import numpy as np

class Tcp_pack:
    def __init__(self, pack_hd=[0]*8, msg=''):
            self.src_port = np.uint16(pack_hd[0]) # 16 bit
            self.dest_port = np.uint16(pack_hd[1]) # 16 bit
            self.seq_num = np.uint32(pack_hd[2]) # 32 bit
            self.ack_num = np.uint32(pack_hd[3]) # 32 bit
            self.misc = np.uint16(pack_hd[4]) # 16 bit for header len and flags
            self.wdw_size = np.uint16(pack_hd[5]) # 16 bit
            self.ck_sum = np.uint16(pack_hd[6]) # 16 bit calc afterwards
            self.ug_ptr = np.uint16(pack_hd[7]) # 16 bit urgent ptr not used
            self.msg = msg
    def set_ports(self, src_port, dest_port):
        self.src_port = np.uint16(src_port)
        self.dest_port = np.uint16(dest_port) 
    def get_ports(self):
        return (self.src_port, self.dest_port)
    
    def set_seq_num(self, seq_num):
        self.seq_num = np.uint32(seq_num)
    def get_seq_num(self):
        return self.seq_num
    
    def set_ack_num(self, ack_num):
        self.ack_num = np.uint32(ack_num)
    def get_ack_num(self):
        return self.ack_num
    
    def set_misc(self, dat_off, flg):
        self.misc = np.uint16("{0:04b}000{1:09b}".format(dat_off, flg))
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
    
    '''convert a pack to hex string'''
    def pack_to_str(self):
        header = '{0:04x}{1:04x}{2:08x}{3:08x}{4:04x}{5:04x}{6:04x}'\
        .format(self.src_port, self.dest_port, self.seq_num, 
                self.ack_num, self.misc, self.wdw_size, self.ck_sum, self.ug_ptr)
        return (header+self.msg)
    
    '''send a packet to addr_port via sock'''
    def send_pack(self, sock, addr_port):
        sock.sendto(self.pack_to_str().encode(), addr_port)         
    
    '''initialize header and return msg'''    
    def recv_msg(self, sock):
        recv_msg = sock.recvfrom(1024)[0].decode()
        header = recv_msg[:40]
        msg = recv_msg[40:]
        tokens = []
        tokens.append(header[0:4])
        tokens.append(header[5:8])
        tokens.append(header[9:16])
        tokens.append(header[17:24])
        tokens.append(header[25:28])
        tokens.append(header[29:32])
        tokens.append(header[33:36])
        tokens.append(header[37:40])
        
        self.__init__([int(i, 16) for i in tokens])
        return msg
                
def iptoint(ip):
    return np.uint32(socket.inet_aton(ip).encode('hex'),16)

def inttoip(ip):
    return socket.inet_ntoa(hex(ip)[2:].decode('hex'))

"""
    start and dest: (ip, port)
    assume initial window size 5840 byte
    assume initial packet size 1400 byte
"""

def cli_listen(start, dest):
    init_head = Tcp_pack()
    init_head.set_ports(start[1], dest[1])# from port to port
    init_head.set_seq_num(0)
    init_head.set_ack_num(0)
    init_head.set_misc(5, 0x02) # data offset unknown yet, so bit set later
    init_head.set_wdw_size(5840)
    init_head.set_ck_sum(0x0) #check sum not known yet initial to 0 calc later
    # set syn to 1
    # calculate check sum
    # send out to srv 
    
    # recv from srv
    # if estab: send back estab
def srv_listen(start, dest):
    # recv udp
    # similar to cli
    
    #recv from cli
    # if estab: estabbed


        
        

'''Provide a hex string return check sum'''
def check_sum_16bit(str):
    for 
        
    






























































