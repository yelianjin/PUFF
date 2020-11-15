# -*- coding:UTF-8 -*-
import socket
import string
import random
import sys
server_ip=sys.argv[1]
port=10000+int(sys.argv[2])
#address=(server_ip,port)
address=(server_ip,port)
#readdr=('219.223.189.207',10000)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(address)
s.listen(5)
while True:
    #print('restart')
    c,addr=s.accept()
    block_size=87380
    #b=''.join(random.sample(string.ascii_letters*1000+string.digits*1000,1024*random.randint(1,15)))
    #c.sendto(b.encode())
    count=0
    c.send('HI'.encode())
    while True:
        #print(block_size)
        data=c.recv(block_size)
        #print(data)
        #print(data[-4:])
        #print(data.decode())
        #print(len(data))
        count+=len(data)
        if(data[-4:]==b'quit'):
            #print('AAA')
            break
        if not data or len(data)==0:
            break
        #if(block_size<1073741824):
            #block_size*=2
        #count+=len(data)
    c.close()
    #print('stop')
    #print(count)
    #print(count)
s.close()
