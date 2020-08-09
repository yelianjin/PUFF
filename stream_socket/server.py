import socket
import string
import random
import sys
address=(sys.argv[1],10000)
readdr=('219.223.189.204',10000)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(address)
s.listen(5)
while True:
    c,addr=s.accept()
    #b=''.join(random.sample(string.ascii_letters*1000+string.digits*1000,1024*random.randint(1,15)))
    #c.sendto(b.encode())
    c.close()
