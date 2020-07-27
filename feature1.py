# -*- coding:UTF-8 -*-
import sys
import csv
import os
import random
def file_name(file_dir):
    ###L的作用是遍历file_dir/brokennode1-40中/所有的csv文件
    L=[]
    for i in range(brokencount):
        ##这里原版本出错，原版本为file_dir+=('brokennode'+str(i))
        temp_dir=file_dir+('brokennode'+str(i))
        for root,dirs,files in os.walk(temp_dir):
            for file in files:
                if os.path.splitext(file)[1]=='.csv':
                    L.append(os.path.join(root,file))
                    
    
    return L
#global align_all
#align_all={}
def initialize():
    count=brokencount
    for i in range(event):
        temp={}
        for j in range(brokencount):
            temp[j]=0
        align_all[i]=temp
#initialize()
#print(align_all)
def get_time():
    ###对于L中的所有项完成时间同步
    ###时间同步的方式为brokennode0中表示 0断掉 那么brokennode0/s0的时间终点时，brokennode0/s0一定断掉
    ###假设brokentime为t02
    ###brokennode0中 h0在正常时会向其他所有host发ping包
    ##h0(192.168.123.1)和h1(192.178.123.2)来回，认为h0收到一个Ping包和发出同一个ping包的时间的/2，和h1收到的ping包的时间的差，即t01-t11
    ##那么h1上节点的t2时刻即为 t02+t01-t11
    ##那么即可校正时刻
    ##在t2的一个精确小的范围内，比如全局最小值的那个点对齐
    #path='/home/ylj/chinaNet/chinaNet/'
    for i in range(event):
        brokenpoint='s'+str(i)
        broke_path=path+'brokennode'+str(i)

        ##temp{}e.g.temp['s1']是0与1之间的时间差
        temp={}
        
        ##start{}e.g.start['sX']是sX在发生brokennode事件时所对应的时间
        start={}

        ##确定t0,brokennodeX事件中brokennodeX最终关闭的时间
        f0=open(broke_path+'/s'+str(i)+'.csv','r')
        r0=f0.readlines()
        try:
            keys=r0[-1].split(' ')
        except:
            print(i)
            error_all.append(i)
            continue
        print(r0[-1])
        keys=list(filter(None,keys))
        t0=float(keys[1])
        f0.close()

        ##确定t1,t2
        srcip='192.168.123.1'
        f1=open(broke_path+'/s0.csv','r')
        r1=f1.readlines()
        for j in range(brokencount):
            alignpoint='s'+str(j)
            if i==j:
                continue
            alignip='192.168.123.'+str(j+1)
            f2=open(broke_path+'/s'+str(j)+'.csv','r')
            r2=f2.readlines()

            ##time1是<src,des,ping>的第一个包的发出时间
            ##time2是<des,src,ping>的第一个包的收到时间
            time1=0
            time2=0
            

            ##确定s0发出一个Ping被对面收到的时刻t1=(time1+time2)/2
            for l1 in r1:
                keys=l1.split(' ')
                keys=list(filter(None,keys))
                s1=keys[2]
                d1=keys[4]
                p1=keys[5]
                ##count1控制是第一个扫到的<src,des,ping>
                ##count2控制是第一个扫到的<des,src,ping>
                count1=0
                count2=0
                if(s1==srcip and d1==alignip and p1=='ICMP' and count1==0):
                    time1=keys[1]
                    count1=1
                if(d1==srcip and s1==alignip and p1=='ICMP' and count2==0):
                    time2=keys[1]
                    count2=1
                if(count1==1 and count2==1):
                    break
            t1=(float(time1)+float(time2))/2
            
            ##确定dst收到s0收到ping的时刻t2
            t2=0
            for l2 in r2:
                keys=l2.split(' ')
                keys=list(filter(None,keys))
                s1=keys[2]
                d1=keys[4]
                p1=keys[5]
                count1=0
                if(s1==srcip and d1==alignip and p1=='ICMP' and count1==0):
                    t2=keys[1]
                    count1=1
                if(count1==1):
                    break
            
            ##temp[s1]为s0和s1之间的时间差
            temp['s'+str(j)]=float(t2)-float(t1)
            
            f2.close()
        temp[brokenpoint]=0

        ##开始建立start{}
        for j in range(brokencount):
            start['s'+str(j)]=t0+temp['s'+str(j)]-temp[brokenpoint]
        print(i)
        print(start)
        align_all[brokenpoint]=start
        f1.close()



def process():
    for i in range(event):
        path1=path+'brokennode'+str(i)
        if i in error_all:
            continue
        ###interval 每次采样的时间窗口的大小，单位为s
        ###head 取（0,1）内的随机数
        ###tail=1-head
        ###count 窗口数量
        interval=0.1
        head=random.random()
        tail=1-head
        count=4
        for j in range(brokencount):
            path2=path1+'/s'+str(j)+'.csv'
            f0=open(path2,'r')
            ##interval 采样窗口
            ##count 采样数量
            #f1=open(path1+'/s'+str(j)+'.txt','w')
            r0=f0.readlines()
            start=align_all['s'+str(i)]['s'+str(j)]-head*interval
            end=start+interval
            time_start=[]
            time_end=[]
            file_list=[]
            for k in range(count):
                ###这里的count/2是指[start,brokennode,end]事件，同时[T0],[T1],[start,brokennode,end],[T4]事件，以4个连续时间的变量为例，先讨论4个连续时间的变量的问题。
                time_start.append(start-(count/2-k)*interval)
                time_end.append(end-(count/2-k)*interval)
                f=open(path1+'/s'+str(j)+'-'+str(k)+'.txt','w')
                file_list.append(f)
            for l0 in r0:
                keys=l0.split(' ')
                keys=list(filter(None,keys))
                header=''
                for temp in keys[7:]:
                    header+=temp.strip()+' '
                time_now=float(keys[1])
                for k in range(count):
                    if(time_now<=time_end[k] and time_now>=time_start[k]):
                        file_list[k].write(keys[1]+'\t'+keys[2]+'\t'+keys[3]+'\t'+keys[4]+'\t'+keys[5]+'\t'+keys[6]+'\t'+header+'\n')
            for k in range(count):
                file_list[k].close()
            f0.close()
            




if __name__ =='__main__':
    global align_all
    align_all={}
    global error_all
    error_all=[]
    global brokencount
    brokencount=42
    global event
    event=28
    initialize()
    global path
    path=''
    #path='/home/ylj/GEANT/test_data/'
    get_time()
    for i in align_all:
        print(align_all[i])
    print('0')
    print(align_all['s0'])
    print(align_all['s0']['s0'])
    print(error_all)
    for i in range(event):
        if i in error_all:
            continue
        print(align_all['s'+str(i)]['s'+str(i)])
    
    process()
    print("error is")
    print(error_all)

