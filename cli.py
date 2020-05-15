import socket
import tcp

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
    
    

if __name__ == "__main__":    
    send_to = ("127.0.0.1", 20002)
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    cli_listen(("127.0.0.1", 20001), ("127.0.0.1", 20002), sock, send_to)



   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
            