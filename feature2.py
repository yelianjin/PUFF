# -*- coding:UTF-8 -*-
import sys
from collections import defaultdict

def selfadd2dimDict(theDict, key_a, key_b):
    # 功能：将int型字典theDict中索引对{key_a:{key_b:val}}所对应的值自加1
    # 备注：因为解释器不能确定第一维的索引是否已经存在于字典theDict中，所以对二维字典直接赋值会报错（类似二维数组），需如下做才能成功添加索引对

    if key_a in theDict:
        if key_b in theDict[key_a]:
            theDict[key_a][key_b] += 1
        else:
            theDict[key_a].update({key_b: 1})
    else:
        theDict.update({key_a: {key_b: 1}})


brokennode_list=[]
global brokencount
brokencount=42
global event
event=42
for i in range(event):
    path='brokennode'+str(i)
    brokennode_list.append(path)
##count采样数量需要与feature1.py中的参数对齐
global wind_count
wind_count=8
for path in brokennode_list:
    for i in range(brokencount):
        tcp_source = defaultdict(int)
        tcp_target = defaultdict(int)
        tcp_count = defaultdict(int)
        retra_count = defaultdict(int)
        icmp_source = defaultdict(int)
        arp_source = defaultdict(int)
        arp_target = defaultdict(int)
        pair = defaultdict(int)
        flag = defaultdict(int)
        retra_source = defaultdict(int)
        retra_target = defaultdict(int)

        for k in range(wind_count): 
            path_txt=path+'/s'+str(i)+'-'+str(k)+'.txt'
            f=open(path_txt,'r')

            tcp_source[str(k)] = {}
            tcp_target[str(k)] = {}
            retra_source[str(k)] = {}
            retra_target[str(k)] = {}

            ###进行IP-sketch
            ###
            count_tcp=0
            count_pair=0
            count_arp_source=0
            count_arp_target=0

            ##tcp_count 对tcp包计数
            ##retra_count 对retra包计数
            tcp_count[str(k)]=0
            retra_count[str(k)]=0
            for item in f:
                keys=item.split('\t')
                if(len(keys)<=4):
                    continue
                if(keys[4]=='TCP'):
                    temp_source=keys[1]
                    temp_target=keys[3]
                    selfadd2dimDict(tcp_source, str(k), temp_source)
                    selfadd2dimDict(tcp_target, str(k), temp_target)
                    tcp_count[str(k)]+=1

                p6=keys[6].strip()
                retra='[TCP Retransmission]'
                temp=p6[:len(retra)]
                if(temp==retra):
                    selfadd2dimDict(retra_source, str(k), keys[1])
                    selfadd2dimDict(retra_target, str(k), keys[3])
                    retra_count[str(k)]+=1
            f.close()


        for k in range(wind_count):
            path_result = path + '/s' + str(i) + '-' + str(k) + '_1.txt'
            f_result = open(path_result, 'w')

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
                f1=0
                f2=0
                f3=0
                f4=0
                f5=0
                f6=0

                # 新添加的特征
                is_first_window = 1 if k == 0 else 0  # 当前窗口是否是第一个窗口

                ratio_tcp_src_prev = 1  # 当前窗口与前一个窗口中IP_source的比值
                if k == 0 and ip not in tcp_source[str(k)]:  # case:当前窗口是第一个窗口，且无IP_source
                    ratio_tcp_src_prev = 0
                if k != 0:
                    if ip not in tcp_source[str(k)]:  # case:当前窗口中无IP_source
                        ratio_tcp_src_prev = 0
                    elif ip not in tcp_source[str(k-1)]:  # case:前一个窗口中无IP_source
                        ratio_tcp_src_prev = tcp_source[str(k)][ip] + 1
                    else:
                        ratio_tcp_src_prev = (tcp_source[str(k)][ip]+1)/(float(tcp_source[str(k-1)][ip]+1))

                ratio_tcp_tar_prev = 1  # 当前窗口与前一个窗口中IP_target的比值
                if k == 0 and ip not in tcp_target[str(k)]:  # case:当前窗口是第一个窗口，且无IP_target
                    ratio_tcp_tar_prev = 0
                if k != 0:
                    if ip not in tcp_target[str(k)]:  # case:当前窗口中无IP_target
                        ratio_tcp_tar_prev = 0
                    elif ip not in tcp_target[str(k-1)]:  # case:前一个窗口中无IP_target
                        ratio_tcp_tar_prev = tcp_target[str(k)][ip] + 1
                    else:
                        ratio_tcp_tar_prev = (tcp_target[str(k)][ip]+1)/(float(tcp_target[str(k-1)][ip]+1))

                is_last_window = 1 if k == wind_count-1 else 0  # 当前窗口是否是最后一个窗口

                ratio_tcp_src_next = 1  # 当前窗口与后一个窗口中IP_source的比值
                if k == wind_count-1 and ip not in tcp_source[str(k)]:  # case:当前窗口是最后一个窗口，且无IP_source
                    ratio_tcp_src_next = 0
                if k != wind_count-1:
                    if ip not in tcp_source[str(k)]:  # case:当前窗口中无IP_source
                        ratio_tcp_src_next = 0
                    elif ip not in tcp_source[str(k+1)]:  # case:后一个窗口中无IP_source
                        ratio_tcp_src_next = tcp_source[str(k)][ip] + 1
                    else:
                        ratio_tcp_src_next = (tcp_source[str(k)][ip]+1)/(float(tcp_source[str(k+1)][ip]+1))
                
               # print(k-1)
                ratio_tcp_tar_next = 1  # 当前窗口与后一个窗口中IP_target的比值
                if k == wind_count-1 and ip not in tcp_target[str(k)]:  # case:当前窗口是最后一个窗口，且无IP_target
                    ratio_tcp_tar_next = 0
                if k != wind_count-1:
                    if ip not in tcp_target[str(k)]:  # case:当前窗口中无IP_target
                        ratio_tcp_tar_next = 0
                    elif ip not in tcp_target[str(k+1)]:  # case:后一个窗口中无IP_target
                        ratio_tcp_tar_next = tcp_target[str(k)][ip] + 1
                    else:
                        ratio_tcp_tar_next = (tcp_target[str(k)][ip]+1)/(float(tcp_target[str(k+1)][ip]+1))

                """
                if(tcp_count!=0):
                    f1=tcp_source[ip]/tcp_count
                    f2=tcp_target[ip]/tcp_count
                    #f1=tcp_source[ip]
                    #f2=tcp_target[ip]
                    f5=1
                """
                if ip not in tcp_source[str(k)]:
                    f1 = 0
                else:
                    f1=tcp_source[str(k)][ip]
                if ip not in tcp_target[str(k)]:
                    f2 = 0
                else:
                    f2=tcp_target[str(k)][ip]
                f5=tcp_count[str(k)]
                if(retra_count[str(k)]!=0):
                    if ip not in retra_source[str(k)]:
                        f3 = 0
                    else:
                        f3=retra_source[str(k)][ip]/retra_count[str(k)]
                    if ip not in retra_target[str(k)]:
                        f4 = 0
                    else:
                        f4=retra_target[str(k)][ip]/retra_count[str(k)]
                    f6=1
                try:
                    f_result.write(str(j-1)+'\t'+ip+'\t'+str(f1)+'\t'+str(f2)+'\t'+str(f3)+'\t'+str(f4)+'\t'+str(f5)+'\t'+str(f6)+'\t'+
                                   str(is_first_window)+'\t'+str(ratio_tcp_src_prev)+'\t'+str(ratio_tcp_tar_prev)+'\t'+
                                   str(is_last_window)+'\t'+str(ratio_tcp_src_next)+'\t'+str(ratio_tcp_tar_next)+'\n')
                except:
                    print(ip)
            f_result.close()
