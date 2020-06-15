import select
import socket
import sys
import queue

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address, file=sys.stderr)
server.bind(server_address)

# Listen for incoming connections
server.listen(5)

conn_remo = [server]
conn_loco = []
msg_que = {} # a dict for all queues
select_timeout = 1
    
while conn_remo:
    print('\nwaiting for the next event', file=sys.stderr)

    readable, writable, exceptional = select.select(conn_remo, conn_loco, conn_remo, select_timeout)
    
    # handle read in
    for s in readable: # handle msg to come
        if s is server: # readable self means a new conn request
            connection, client_address = s.accept() # accept an incoming conn request
            print('new connection from {}'.format(client_address), file=sys.stderr)
            connection.setblocking(0)# non-block
            conn_remo.append(connection) # add to list of accepted incoming conn
            msg_que[connection] = queue.Queue() # assign a queue to this conn for incoming msg
        else: # actual msg income
            data = s.recv(1024)
            if data:
                print('received \"{}\" from {}'.format(data.decode('utf-8'), s.getpeername()), file=sys.stderr)
                msg_que[s].put(data) # save income msg to its assigned queue
                if s not in conn_loco: # Add output channel for response (TODO)
                    conn_loco.append(s)
            else: # no data, attempt to close
                print('closing {}.'.format(client_address), file=sys.stderr)
                if s in conn_loco: # clear from in and out
                    conn_loco.remove(s)
                conn_remo.remove(s)
                del msg_que[s] # Remove message queue
                s.close()
    # handle write out
    for s in writable: # handle msg to leave
        try:
            next_msg = msg_que[s].get_nowait()   # send out whatever client provides (TODO)
        except queue.Empty: # no message at all
            print('output queue for {} is empty'.format(s.getpeername()), file=sys.stderr)
            conn_loco.remove(s)
        else:   # got something
            print('sending \"{}\" to {}'.format(next_msg, s.getpeername()), file=sys.stderr)
            s.send(next_msg)
    # Handle exceptions
    for s in exceptional:
        print('exception for {}'.format(s.getpeername()), file=sys.stderr)
        conn_remo.remove(s) # Stop listening for input on the connection
        if s in conn_loco:
            conn_loco.remove(s)
        s.close()
        del msg_que[s] # Remove message queue
    # handle timeout
    if not (readable or writable or exceptional):
        print('timed out, do some other work here', file=sys.stderr)
        continue







