import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print(server_address)
sock.bind(server_address)

ip = False

while ip is False:
    print('waiting to receive message')
    data, address = sock.recvfrom(4096)
    
    print ('received ' + str(len(data)) + ' bytes from ' + str(address))
    print(data)
    
    if data:
        sent = sock.sendto(data, address)
        print('sent ' + str(sent) + ' bytes back to ' + str(address))
        ip = address

while True:
    sock.sendto(bytearray("hello", 'utf-8'), ip)