import socket
import tcp


send_to = ("127.0.0.1", 20001)
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

pack = tcp.Tcp_pack()        
pack.set_ports(36869, 32412)
pack.set_seq_num(19125)
pack.set_ack_num(0)
pack.set_misc(6, 0x02)
pack.set_wdw_size(8760)
pack.set_ck_sum(0xa92c)

pack.send_pack(sock, send_to)

new_pack = tcp.Tcp_pack()
new_pack.recv_pack(sock)
print("Old: {} New {}".format(pack.get_ck_sum(), new_pack.get_ck_sum()))
  
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
            