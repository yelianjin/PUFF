from scapy.all import *
import random
import sys
dst_IP=sys.argv[1]
interval=0.1
count_pkt=random.randint(2,10)
size=1448
data=Raw(RandString(size))
print(data)
print(size)
print(dst_IP)
print(count_pkt)
sport=5555
dport=6666
"""
#test
ip=IP(dst=dst_IP)
test=TCP(sport=sport,dport=dport,seq=1)/data
print(len(test.payload))
test2=TCP(sport=sport,dport=dport,seq=1+len(test.payload))/data
print(len(test2.payload))
print("2")
"""
#SYN
ip=IP(dst=dst_IP)
SYN=TCP(sport=sport,dport=dport,flags='S',seq=100)
SYNACK=sr1(ip/SYN)
#ACK
ACK=TCP(sport=sport,dport=dport,flags='A',ack=SYNACK.seq+1,seq=SYNACK.ack)
send(ip/ACK)
tcpACK=SYNACK
#data
for interval in range(count_pkt):
    end_tcp=101+interval*len(data)
    #sr method
    tcp=TCP(sport=sport,dport=dport,flags='PA',seq=end_tcp)/data
    send(ip/tcp)
    #send
#FIN
FIN=TCP(sport=sport,dport=dport,flags='FA',seq=end_tcp+len(data))
FINACK=sr1(ip/FIN)
LASTACK=TCP(sport=sport,dport=dport,flags='A',seq=FINACK.ack,ack=FINACK.seq+1)
send(LASTACK)
