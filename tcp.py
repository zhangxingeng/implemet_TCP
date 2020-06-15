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
    def seq_num_inc(self):
        self.seq_num = self.seq_num + 1
    
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
    
    def set_msg(self, msg=''):
        self.msg = msg
    def get_msg(self):
        return self.msg
    def get_msg_len(self):
        return len(self.msg)
    
    '''convert a pack to hex string'''
    def pack_to_str(self):
        header = '{0:04x}{1:04x}{2:08x}{3:08x}{4:04x}{5:04x}{6:04x}{7:04x}'\
        .format(self.src_port, self.dest_port, self.seq_num, 
                self.ack_num, self.misc, self.wdw_size, self.ck_sum, self.ug_ptr)
        return (header+self.msg)
    
        '''Provide a hex string return check sum'''
    def check_sum_16bit(self):
        pack_str = self.pack_to_str()
        cksum = np.uint16(0)
        for i in range(0, len(pack_str), 4):
            cksum = cksum + np.uint16(int(pack_str[i:i+4], base=16))
            self.ck_sum = cksum
        return cksum

    '''send a packet to addr_port via sock'''
    def send_pack(self, sock, addr_port):
        try:
            sock.sendto(self.pack_to_str().encode(), addr_port)
        except:
            raise Exception("send_fail")         
    
    '''initialize header and return msg'''    
    def recv_pack(self, sock):
        try:
            recv = sock.recvfrom(1024)
            recv_msg = recv[0].decode()
            header = recv_msg[:40]
            self.msg = recv_msg[40:]
            tokens = []
            tokens.append(header[0:4])
            tokens.append(header[4:8])
            tokens.append(header[8:16])
            tokens.append(header[16:24])
            tokens.append(header[24:28])
            tokens.append(header[28:32])
            tokens.append(header[32:36])
            tokens.append(header[36:40])
            #print(recv_msg)
            #print(tokens)
            self.__init__([int(i, base=16) for i in tokens])
            return recv[1]
        except:
            raise Exception("recv_fail")
            return None
        
    def print_pack(self):
        print("from_port: {} to_port: {}".format(self.src_port, self.dest_port))
        print("seq_num: {} ack_num: {}".format(self.seq_num, self.ack_num))
        print("misc: {} wdw_size: {}".format(self.misc, self.wdw_size))
        print("ck_sum: {} urgent_ptr: {}".format(self.ck_sum, self.ug_ptr))
        print("msg: {}".format(self.msg))
        
                
def iptoint(ip):
    return np.uint32(socket.inet_aton(ip).encode('hex'),16)

def inttoip(ip):
    return socket.inet_ntoa(hex(ip)[2:].decode('hex'))





        
        


        
    
        
    






























































