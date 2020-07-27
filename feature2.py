# -*- coding:UTF-8 -*-
import sys
from collections import defaultdict
brokennode_list=[]
global brokencount
brokencount=42
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

            ##tcp_count 对tcp包计数
            ##retra_count 对retra包计数
            tcp_count=0
            retra_count=0
            for item in f:
                keys=item.split('\t')
                if(len(keys)<=4):
                    continue
                if(keys[4]=='TCP'):
                    temp_source=keys[1]
                    temp_target=keys[3]
                    tcp_source[temp_source]+=1
                    tcp_target[temp_target]+=1
                    tcp_count+=1

                p6=keys[6].strip()
                retra='[TCP Retransmission]'
                temp=p6[:len(retra)]
                if(temp==retra):
                    retra_source[keys[1]]+=1
                    retra_target[keys[3]]+=1
                    retra_count+=1
            f.close()   
            ###对于IP_source和IP_target进行统计

            ###记录结果
            for j in range(1,brokencount+1):
                ###该窗口内的信息
                ###f1:tcp_src占所有TCP的比例
                ###f2:tcp_dst占所有TCP的比例
                ###f3:retra_src占所有retra包的比例
                ###f4:retra_target占所有retra包的比例
                ###f5:是否有TCP包
                ###f6:是否有retra包
                ip='192.168.123.'+str(j)
                f1=1
                f2=1
                f3=0
                f4=0
                f5=0
                f6=0
                if(tcp_count!=0):
                    f1=tcp_source[ip]/tcp_count
                    f2=tcp_target[ip]/tcp_count
                    f5=1
                if(retra_count!=0):
                    f3=retra_source[ip]/retra_count
                    f4=retra_target[ip]/retra_count
                    f6=1
                try:
                    f_result.write(str(j-1)+'\t'+ip+'\t'+str(f1)+'\t'+str(f2)+'\t'+str(f3)+'\t'+str(f4)+'\t'+str(f5)+'\t'+str(f6)+'\n')
                except:
                    print(ip)
            f_result.close()
