import socket
import sys

messages = ['This is the message. ', 'It will be sent ', 'in parts.',]
server_address = ('localhost', 10000)
socks = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM),
          socket.socket(socket.AF_INET, socket.SOCK_STREAM),]
print('connecting to %s port %s' % server_address, file=sys.stderr)

for s in socks: # connect to all ports
    s.connect(server_address)
    
for message in messages: # Send messages on both sockets
    for s in socks:
        print('%s: sending "%s"' % (s.getsockname(), message), file=sys.stderr)
        s.send(message.encode('utf-8'))

    # Read responses on both sockets
    for s in socks:
        data = s.recv(1024).decode('utf-8')
        print('%s: received "%s"' % (s.getsockname(), data), file=sys.stderr)
        if not data:
            print('closing socket', s.getsockname(), file=sys.stderr)
            s.close()