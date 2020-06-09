# -*- coding:UTF-8 -*-
import sys
from collections import defaultdict
brokennode_list=[]
global brokencount
brokencount=40
for i in range(brokencount):
    path='brokennode'+str(i)
    brokennode_list.append(path)
##count采样数量需要与feature1.py中的参数对齐
global count
count=4
for path in brokennode_list:
    for i in range(brokencount):
        for k in range(count): 
            path_txt=path+'/s'+str(i)+'-'+str(k)+'.txt'
            f=open(path_txt,'r')
            path_result=path+'/s'+str(i)+'-'+str(k)+'_1.txt'
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


                p6=keys[6].strip()
                retra='[TCP Retransmission]'
                temp=p6[:len(retra)]
                if(temp==retra):
                    retra_source[keys[1]]+=1
                    retra_target[keys[3]]+=1
            f.close()   
            ###对于IP_source和IP_target进行统计

            ###记录结果
            for j in range(1,brokencount+1):
                ip='192.168.123.'+str(j)
                f_result.write(str(j-1)+'\t'+ip+'\t'+str(retra_source[ip])+'\t'+str(retra_target[ip])+'\t'+str(tcp_source[ip])+'\t'+str(tcp_target[ip])+'\n')

            f_result.close()
