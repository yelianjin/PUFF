# -*- coding:UTF-8 -*-
import sys
from collections import defaultdict
brokennode_list=[]
global brokencount
brokencount=42
for i in range(brokencount):
    path='brokennode'+str(i)
    brokennode_list.append(path)
for path in brokennode_list:
    for i in range(brokencount):
        path_txt=path+'/s'+str(i)+'.txt'
        f=open(path_txt,'r')
        path_result=path+'/s'+str(i)+'_1.txt'
        f_result=open(path_result,'w')
        tcp_source=defaultdict(int)
        tcp_target=defaultdict(int)
        icmp_source=defaultdict(int)
        arp_source=defaultdict(int)
        arp_target=defaultdict(int)
        pair=defaultdict(int)
        flag=defaultdict(int)
        retra_source=defaultdict(int)
        retra_target=defaultdict(int)
        ###进行IP-sketch
        ###
        count_tcp=0
        count_pair=0
        count_arp_source=0
        count_arp_target=0
        for item in f:
            keys=item.split('\t')
            if(len(keys)<=4):
                continue
            if(keys[4]=='TCP'):
                temp_source=keys[1]
                temp_target=keys[3]
                tcp_source[temp_source]+=1
                tcp_target[temp_target]+=1

            if(keys[4]=='ARP'):
                source=keys[1]
                target=keys[3]
                if source not in arp_source:
                    arp_source[source]+=1
                    count_arp_source+=1
                if target not in arp_target:
                    arp_target[target]+=1
                    count_arp_target+=1

            p6=keys[6].strip()
            retra='[TCP Retransmission]'
            temp=p6[:len(retra)]
            if(temp==retra):
                retra_source[keys[1]]+=1
                retra_target[keys[3]]+=1
        f.close()   
        ###对于IP_source和IP_target进行统计
        ###flag[j]标志不相等的情况用以控制pair[ip]
        """
        for j in range(1,41):
            ip='192.168.123.'+str(j)
            try:
                pair[ip]=float(tcp_source[ip]*100/tcp_target[ip])
            except:
                pair[ip]=0
            if (tcp_source[ip]!=tcp_target[ip]):
                flag[ip]=1
            else:
                flag[ip]=0
        """
        ###记录结果
        for j in range(1,brokencount+1):
            ip='192.168.123.'+str(j)
            f_result.write(str(j-1)+'\t'+ip+'\t'+str(retra_source[ip])+'\t'+str(retra_target[ip])+'\t'+str(tcp_source[ip])+'\t'+str(tcp_target[ip])+'\n')

        f_result.close()
