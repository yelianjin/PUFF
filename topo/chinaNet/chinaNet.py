# -*- coding:UTF-8 -*-
#!/usr/bin/python

"""
Custom topology for Mininet, generated by GraphML-Topo-to-Mininet-Network-Generator.
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Node
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections
from time import sleep
from mininet.util import quietRun
from mininet.log import setLogLevel,info
import random
import sys
import time
import os
from threading import Thread
import multiprocessing
from scapy.all import *
##Build Your Topo
class GeneratedTopo(Topo):
    "Internet Topology Zoo Specimen."

    def __init__(self, **opts):
        "Create a topology."

        # Initialize Topology
        Topo.__init__(self, **opts)

        # add nodes, switches first...
        Lhasa = self.addSwitch('s0',failMode='standalone',stp=True)
        Lanzhou = self.addSwitch('s1',failMode='standalone',stp=True)
        Kashi = self.addSwitch('s2',failMode='standalone',stp=True)
        Shiquanhe = self.addSwitch('s3',failMode='standalone',stp=True)
        Jinan = self.addSwitch('s4',failMode='standalone',stp=True)
        Qingdao = self.addSwitch('s5',failMode='standalone',stp=True)
        Taiyuan = self.addSwitch('s6',failMode='standalone',stp=True)
        Shilazhuang = self.addSwitch('s7',failMode='standalone',stp=True)
        Shanghai = self.addSwitch('s8',failMode='standalone',stp=True)
        Suzhou = self.addSwitch('s9',failMode='standalone',stp=True)
        InternationalLink1 = self.addSwitch('s10',failMode='standalone',stp=True)
        InternationalLink2 = self.addSwitch('s11',failMode='standalone',stp=True)
        Nanning = self.addSwitch('s12',failMode='standalone',stp=True)
        Changsha = self.addSwitch('s13',failMode='standalone',stp=True)
        Guiyang = self.addSwitch('s14',failMode='standalone',stp=True)
        Chongqing = self.addSwitch('s15',failMode='standalone',stp=True)
        Chengdu = self.addSwitch('s16',failMode='standalone',stp=True)
        Kunming = self.addSwitch('s17',failMode='standalone',stp=True)
        Xian = self.addSwitch('s18',failMode='standalone',stp=True)
        Zhengzhou = self.addSwitch('s19',failMode='standalone',stp=True)
        InternationalLink4 = self.addSwitch('s20',failMode='standalone',stp=True)
        InternationalLink3 = self.addSwitch('s21',failMode='standalone',stp=True)
        Haikou = self.addSwitch('s22',failMode='standalone',stp=True)
        HongKong = self.addSwitch('s23',failMode='standalone',stp=True)
        Hangzhou = self.addSwitch('s24',failMode='standalone',stp=True)
        Wuhan = self.addSwitch('s25',failMode='standalone',stp=True)
        Hefei = self.addSwitch('s26',failMode='standalone',stp=True)
        Nanjing = self.addSwitch('s27',failMode='standalone',stp=True)
        Guangzhou = self.addSwitch('s28',failMode='standalone',stp=True)
        Xiamen = self.addSwitch('s29',failMode='standalone',stp=True)
        Fuzhou = self.addSwitch('s30',failMode='standalone',stp=True)
        Nandhang = self.addSwitch('s31',failMode='standalone',stp=True)
        Xining = self.addSwitch('s32',failMode='standalone',stp=True)
        Urumqi = self.addSwitch('s33',failMode='standalone',stp=True)
        Harbin = self.addSwitch('s34',failMode='standalone',stp=True)
        Changchun = self.addSwitch('s35',failMode='standalone',stp=True)
        Shenyang = self.addSwitch('s36',failMode='standalone',stp=True)
        Dalian = self.addSwitch('s37',failMode='standalone',stp=True)
        Tianjin = self.addSwitch('s38',failMode='standalone',stp=True)
        Beijing = self.addSwitch('s39',failMode='standalone',stp=True)
        Hohhot = self.addSwitch('s40',failMode='standalone',stp=True)
        Yinchuan = self.addSwitch('s41',failMode='standalone',stp=True)

        # ... and now hosts
        Lhasa_host = self.addHost('h0', ip='192.168.123.1')
        Lanzhou_host = self.addHost('h1', ip='192.168.123.2')
        Kashi_host = self.addHost('h2', ip='192.168.123.3')
        Shiquanhe_host = self.addHost('h3', ip='192.168.123.4')
        Jinan_host = self.addHost('h4', ip='192.168.123.5')
        Qingdao_host = self.addHost('h5', ip='192.168.123.6')
        Taiyuan_host = self.addHost('h6', ip='192.168.123.7')
        Shilazhuang_host = self.addHost('h7', ip='192.168.123.8')
        Shanghai_host = self.addHost('h8', ip='192.168.123.9')
        Suzhou_host = self.addHost('h9', ip='192.168.123.10')
        InternationalLink1_host = self.addHost('h10', ip='192.168.123.11')
        InternationalLink2_host = self.addHost('h11', ip='192.168.123.12')
        Nanning_host = self.addHost('h12', ip='192.168.123.13')
        Changsha_host = self.addHost('h13', ip='192.168.123.14')
        Guiyang_host = self.addHost('h14', ip='192.168.123.15')
        Chongqing_host = self.addHost('h15', ip='192.168.123.16')
        Chengdu_host = self.addHost('h16', ip='192.168.123.17')
        Kunming_host = self.addHost('h17', ip='192.168.123.18')
        Xian_host = self.addHost('h18', ip='192.168.123.19')
        Zhengzhou_host = self.addHost('h19', ip='192.168.123.20')
        InternationalLink4_host = self.addHost('h20', ip='192.168.123.21')
        InternationalLink3_host = self.addHost('h21', ip='192.168.123.22')
        Haikou_host = self.addHost('h22', ip='192.168.123.23')
        HongKong_host = self.addHost('h23', ip='192.168.123.24')
        Hangzhou_host = self.addHost('h24', ip='192.168.123.25')
        Wuhan_host = self.addHost('h25', ip='192.168.123.26')
        Hefei_host = self.addHost('h26', ip='192.168.123.27')
        Nanjing_host = self.addHost('h27', ip='192.168.123.28')
        Guangzhou_host = self.addHost('h28', ip='192.168.123.29')
        Xiamen_host = self.addHost('h29', ip='192.168.123.30')
        Fuzhou_host = self.addHost('h30', ip='192.168.123.31')
        Nandhang_host = self.addHost('h31', ip='192.168.123.32')
        Xining_host = self.addHost('h32', ip='192.168.123.33')
        Urumqi_host = self.addHost('h33', ip='192.168.123.34')
        Harbin_host = self.addHost('h34', ip='192.168.123.35')
        Changchun_host = self.addHost('h35', ip='192.168.123.36')
        Shenyang_host = self.addHost('h36', ip='192.168.123.37')
        Dalian_host = self.addHost('h37', ip='192.168.123.38')
        Tianjin_host = self.addHost('h38', ip='192.168.123.39')
        Beijing_host = self.addHost('h39', ip='192.168.123.40')
        Hohhot_host = self.addHost('h40', ip='192.168.123.41')
        Yinchuan_host = self.addHost('h41', ip='192.168.123.42')

        # add edges between switch and corresponding host
        self.addLink(Lhasa, Lhasa_host)
        self.addLink(Lanzhou, Lanzhou_host)
        self.addLink(Kashi, Kashi_host)
        self.addLink(Shiquanhe, Shiquanhe_host)
        self.addLink(Jinan, Jinan_host)
        self.addLink(Qingdao, Qingdao_host)
        self.addLink(Taiyuan, Taiyuan_host)
        self.addLink(Shilazhuang, Shilazhuang_host)
        self.addLink(Shanghai, Shanghai_host)
        self.addLink(Suzhou, Suzhou_host)
        self.addLink(InternationalLink1, InternationalLink1_host)
        self.addLink(InternationalLink2, InternationalLink2_host)
        self.addLink(Nanning, Nanning_host)
        self.addLink(Changsha, Changsha_host)
        self.addLink(Guiyang, Guiyang_host)
        self.addLink(Chongqing, Chongqing_host)
        self.addLink(Chengdu, Chengdu_host)
        self.addLink(Kunming, Kunming_host)
        self.addLink(Xian, Xian_host)
        self.addLink(Zhengzhou, Zhengzhou_host)
        self.addLink(InternationalLink4, InternationalLink4_host)
        self.addLink(InternationalLink3, InternationalLink3_host)
        self.addLink(Haikou, Haikou_host)
        self.addLink(HongKong, HongKong_host)
        self.addLink(Hangzhou, Hangzhou_host)
        self.addLink(Wuhan, Wuhan_host)
        self.addLink(Hefei, Hefei_host)
        self.addLink(Nanjing, Nanjing_host)
        self.addLink(Guangzhou, Guangzhou_host)
        self.addLink(Xiamen, Xiamen_host)
        self.addLink(Fuzhou, Fuzhou_host)
        self.addLink(Nandhang, Nandhang_host)
        self.addLink(Xining, Xining_host)
        self.addLink(Urumqi, Urumqi_host)
        self.addLink(Harbin, Harbin_host)
        self.addLink(Changchun, Changchun_host)
        self.addLink(Shenyang, Shenyang_host)
        self.addLink(Dalian, Dalian_host)
        self.addLink(Tianjin, Tianjin_host)
        self.addLink(Beijing, Beijing_host)
        self.addLink(Hohhot, Hohhot_host)
        self.addLink(Yinchuan, Yinchuan_host)

        # add edges between switches
        self.addLink(Lhasa, Chengdu, bw=10, delay='6.35774246343ms')
        self.addLink(Lhasa, Shiquanhe, bw=10, delay='5.57654200465ms')
        self.addLink(Lhasa, Beijing, bw=10, delay='13.0311447504ms')
        self.addLink(Lanzhou, Xian, bw=10, delay='2.58086291716ms')
        self.addLink(Lanzhou, Beijing, bw=10, delay='6.01439691557ms')
        self.addLink(Kashi, Urumqi, bw=10, delay='5.47496181141ms')
        self.addLink(Jinan, Shanghai, bw=10, delay='3.71953825955ms')
        self.addLink(Qingdao, Tianjin, bw=10, delay='2.23644440406ms')
        self.addLink(Taiyuan, Xian, bw=10, delay='2.62926610752ms')
        self.addLink(Taiyuan, Beijing, bw=10, delay='2.04281460033ms')
        self.addLink(Shilazhuang, Beijing, bw=10, delay='1.34986725695ms')
        self.addLink(Shanghai, Tianjin, bw=10, delay='4.89109791206ms')
        self.addLink(Shanghai, Beijing, bw=10, delay='5.42870203145ms')
        self.addLink(Shanghai, Suzhou, bw=10, delay='0.408837609009ms')
        self.addLink(Shanghai, InternationalLink2, bw=10, delay='0.408837609009ms')
        self.addLink(Shanghai, Chengdu, bw=10, delay='8.4258123639ms')
        self.addLink(Shanghai, Xian, bw=10, delay='6.19260814032ms')
        self.addLink(Shanghai, HongKong, bw=10, delay='10.1803264988ms')
        self.addLink(Shanghai, Hangzhou, bw=10, delay='0.830999214798ms')
        self.addLink(Shanghai, Wuhan, bw=10, delay='3.50478829641ms')
        self.addLink(Shanghai, Hefei, bw=10, delay='2.04395439514ms')
        self.addLink(Shanghai, Nanjing, bw=10, delay='1.37383779989ms')
        self.addLink(Shanghai, Guangzhou, bw=10, delay='6.16024168491ms')
        self.addLink(Shanghai, Nandhang, bw=10, delay='3.08284436302ms')
        self.addLink(Suzhou, Nanjing, bw=10, delay='0.981181716738ms')
        self.addLink(InternationalLink1, Beijing, bw=10, delay='5.22840305025ms')
        self.addLink(Nanning, Guangzhou, bw=10, delay='2.57218638075ms')
        self.addLink(Changsha, Wuhan, bw=10, delay='1.49106954604ms')
        self.addLink(Guiyang, Chengdu, bw=10, delay='2.65523566055ms')
        self.addLink(Guiyang, Guangzhou, bw=10, delay='3.87969350518ms')
        self.addLink(Chongqing, Chengdu, bw=10, delay='1.36590446997ms')
        self.addLink(Chongqing, Guangzhou, bw=10, delay='4.97461050737ms')
        self.addLink(Chengdu, Nanjing, bw=10, delay='7.1361484385ms')
        self.addLink(Chengdu, Guangzhou, bw=10, delay='6.28938517016ms')
        self.addLink(Kunming, Guangzhou, bw=10, delay='5.53922803472ms')
        self.addLink(Xian, Xining, bw=10, delay='3.55520907699ms')
        self.addLink(Xian, Urumqi, bw=10, delay='10.7635773864ms')
        self.addLink(Xian, Yinchuan, bw=10, delay='2.66778714428ms')
        self.addLink(Xian, Beijing, bw=10, delay='4.63624896292ms')
        self.addLink(Xian, Hohhot, bw=10, delay='3.89785999397ms')
        self.addLink(Xian, Wuhan, bw=10, delay='3.28474220522ms')
        self.addLink(Xian, Nanjing, bw=10, delay='4.81936568267ms')
        self.addLink(Xian, Guangzhou, bw=10, delay='6.648208335ms')
        self.addLink(Zhengzhou, Beijing, bw=10, delay='3.16072066923ms')
        self.addLink(InternationalLink4, HongKong, bw=10, delay='6.7784822369ms')
        self.addLink(InternationalLink3, Guangzhou, bw=10, delay='6.58101680184ms')
        self.addLink(Haikou, Wuhan, bw=10, delay='6.2814122388ms')
        self.addLink(Haikou, Guangzhou, bw=10, delay='2.31206298414ms')
        self.addLink(HongKong, Guangzhou, bw=10, delay='7.54650539127ms')
        self.addLink(HongKong, Beijing, bw=10, delay='9.16966260536ms')
        self.addLink(Wuhan, Beijing, bw=10, delay='5.35929661999ms')
        self.addLink(Wuhan, Nanjing, bw=10, delay='2.33206308386ms')
        self.addLink(Nanjing, Beijing, bw=10, delay='4.56460667833ms')
        self.addLink(Nanjing, Fuzhou, bw=10, delay='3.40060941933ms')
        self.addLink(Guangzhou, Tianjin, bw=10, delay='9.2499639818ms')
        self.addLink(Guangzhou, Beijing, bw=10, delay='9.60658994588ms')
        self.addLink(Guangzhou, Xiamen, bw=10, delay='2.61405148976ms')
        self.addLink(Xining, Beijing, bw=10, delay='6.74351506521ms')
        self.addLink(Urumqi, Beijing, bw=10, delay='12.2609371147ms')
        self.addLink(Harbin, Beijing, bw=10, delay='5.37351981527ms')
        self.addLink(Changchun, Beijing, bw=10, delay='4.37060898815ms')
        self.addLink(Shenyang, Beijing, bw=10, delay='3.1890878442ms')
        self.addLink(Dalian, Tianjin, bw=10, delay='1.94685618232ms')
        self.addLink(Tianjin, Beijing, bw=10, delay='0.54992435799ms')
        self.addLink(Beijing, Hohhot, bw=10, delay='2.1055984939ms')
        self.addLink(Beijing, Yinchuan, bw=10, delay='4.50552454992ms')

##Thread of traffic,py
class TrafficThread(Thread):
    def __init__(self,h1,h2):
        self.h1=h1
        self.h2=h2
        Thread.__init__(self)
    def run(self):
        print(self.h1.IP())
        print(self.h2.IP())
        print("HI")
        self.h1.cmd('sudo python /home/ylj/GEANT/test_node/traffic.py %s' % self.h2.IP())

#worker 程序
def worker(h1,h2):
    h1.cmd('sudo python traffic.py '+h2.IP()+' &')
    print('IP is')
    print(h2.IP())

def traffic(net,j):
    list_all=[]
    for i in range(42):
        list_all.append(i)
    list1=random.sample(list_all,21)
    for item in list1:
        if(item in list1):
            list_all.remove(item)
    list2=random.sample(list_all,21)
    f_throughput=open('throughput.txt','a')
    f_throughput.write(str(i)+'\n')
    


    ##加入进程list
    jobs=[]
    for temp in range(21):
        str1=list1[temp]
        for temp2 in range(21):
            str2=list2[temp2]
            h1='h'+str(str1)
            h2='h'+str(str2)
            """
            if(str1==brokennode):
                a=h1
                h1=h2
                h2=a
            print(h1)
            print(h2)
            """
            f_throughput.write(h1+'\t'+h2+'\n')
            node1=net.get(h1)
            node2=net.get(h2)
            print(node1.IP())
            print(node2.IP())
            """
            thread=TrafficThread(node1,node2)
            threads.append(thread)
            thread.start()
            """
        
            p=multiprocessing.Process(target=worker,args=(node1,node2))
            jobs.append(p)
            f_throughput.write('\n')
    ##jobs shuffle
    jobs=random.sample(jobs,len(jobs))
    ##jobs start
    count=0
    stop=int(len(jobs)*3/4)
    for p in jobs:
        p.start()
        ### close signal
        if(count==stop):
            pingtest(net,42)
            singledown(net,0,brokennode)
        count+=1
    sleep(1)
    ##wait for close signal
    for p in jobs:
        print("Try to close subprocess")
        p.terminate()
    start=time.time()
    judge=start
    while True:
        print('Kill me')
        if(judge-start>=0.5):
            f_throughput.close()
            net.stop()
            sys.exit(0)
            break

        judge+=1

def pingtest(net,n):
    h0=net.hosts[0]
    for i in range(1,n):
        h1=net.hosts[i]
        h0.cmdPrint('ping -Q 0x64 -c 1 '+h1.IP())
    print("PING is OK")

def singledown(net,i,brokennode):
    #count=random.randint(0,41)
    #count=5
    count=brokennode
    node1='s'+str(count)
    node1_neighbors=neighbors[node1]
    print(node1)
    f_brokenswitch=open("brokenswitch.txt",'a')
    f_brokenswitch.write(str(i)+'\t'+node1+'\t')
    for node2 in node1_neighbors:
        print(node2)
        f_brokenswitch.write(node2+'\t')
        net.configLinkStatus(node1,node2,'down')
    f_brokenswitch.write('\n')
    #normal(net,i)
    f_brokenswitch.close()
    print('i have closed')
 


def normal(net,j):
    list_all=[]
    for i in range(40):
        list_all.append(i)
    list1=random.sample(list_all,20)
    for item in list1:
        if(item in list1):
            list_all.remove(item)
    list2=random.sample(list_all,20)
    f_throughput=open('throughput.txt','a')
    f_throughput.write(str(i)+'\n')
    for temp in range(20):
        str1=list1[temp]
        for temp2 in range(1):
            str2=list2[temp2]
            h1='h'+str(str1)
            h2='h'+str(str2)
            if(str1==brokennode):
                a=h1
                h1=h2
                h2=a
            print(h1)
            print(h2)
            f_throughput.write(h1+'\t'+h2+'\n')
            node1=net.get(h1)
            node2=net.get(h2)
            print(node1.IP())
            print(node2.IP())
            data=Raw(RandString(size=1600))
            #node1.cmd("iperf "+'-t 10 -c '+node2.IP()+" & ")
            pkt=IP(src=node1.IP(),dst=node2.IP())/TCP(sport=12345,dport=12345)/data
            send(pkt,inter=0.05,count=1)
        f_throughput.write('\n')
    f_throughput.close()


def brokenlink(net,i):
    dic_keys={}
    f_brokenlink=open('brokenlink.txt','a')
    s_w=random.randint(0,1)
    count=random.randint(2,40)
    node1=''
    if(s_w==0):
        node1='s'+str(count)
    if(s_w==1):
        node1='h'+str(count)
    print(type(node1))
    print(node1)
    if(s_w==0):
        node2=random.choice(neighbors[node1])
    if(s_w==1):
        node2='s'+str(count)
    print(type(node2))
    print(node2)
    f_brokenlink.write(str(i)+'\t'+node1+'\t'+node2+'\t'+'\n')
    f_brokenlink.close()
    net.configLinkStatus(node1,node2,'down')
    normal(net,i)
    sleep(1)
    net.configLinkStatus(node1,node2,'up')
    sleep(2)
    """
    for item1 in net.switches:
        node1=item1.name
        for item2 in neighbors[node1]:
            if(item2[0]=='h'):
                continue
            node2=item2
            print(node1)
            print(node2)
            temp1=node1+'\t'+node2
            temp2=node2+'\t'+node1
            if(temp1 in dic_keys):
                continue
            else:
                dic_keys[temp1]=1
                dic_keys[temp2]=1
            f_brokenlink.write(str(count)+'\t'+node1+'\t'+node2+'\t'+'\n')
            f_brokenlink.close()
            net.configLinkStatus(node1,node2,'down')
            net.pingAll()
            sleep(1)
            net.configLinkStatus(node1,node2,'up')
            count+=1
    """
def brokenlink1(net,node1,node2):
    print(node1)
    print(node2)
    f_brokenlink.write(node1+'\t'+node2+'\t'+'\n')
    net.configLinkStatus(node1,node2,'down')
    net.pingAll()
    sleep(1)
    net.configLinkStatus(node1,node2,'up')
def brokenswitch(net,i,brokennode):
    #count=random.randint(0,41)
    #count=5
    count=brokennode
    node1='s'+str(count)
    node1_neighbors=neighbors[node1]
    print(node1)
    f_brokenswitch=open("brokenswitch.txt",'a')
    f_brokenswitch.write(str(i)+'\t'+node1+'\t')
    for node2 in node1_neighbors:
        print(node2)
        f_brokenswitch.write(node2+'\t')
        net.configLinkStatus(node1,node2,'down')
    f_brokenswitch.write('\n')
    normal(net,i)
    f_brokenswitch.close()
    #sleep(1)
    for node2 in node1_neighbors:
        net.configLinkStatus(node1,node2,'up')
    #sleep(2)
def myNet():
    global brokennode
    brokennode=sys.argv[1]
    print(brokennode)
    net = Mininet(topo=GeneratedTopo(), controller=lambda a: RemoteController(a,ip='127.0.0.1',port=6633),host=CPULimitedHost,link=TCLink)
    #net=Mininet(topo=GeneratedTopo(),host=CPULimitedHost,link=TCLink)
    #net.addController('c0', RemoteController, ip="127.0.0.1",port=6633)
    print("Hello")
    #net.start()
    print("DUmping host coonnections")
    #dumpNodeConnections(net.hosts)
    net.start()
    print("host is OKJ")
    #sleep(10)
    while 'is_connected' not in quietRun('ovs-vsctl show'):
        sleep(1)
        print('.')
    print("Test pingall")
    print(type(net.hosts))
    print(type(net.links))
    global neighbors
    neighbors={}
    global mac
    mac={}
    f_neighbors=open('neighbors.txt','w')
    f_mac=open('mac.txt','w')
    for item in net.hosts:
        list_host=[]
        host_mac={}
        print(type(item.name))
        print(item.name)
        neighbors[item.name]=list_host
        mac[item.name]=host_mac
    for item in net.switches:
        list_switch=[]
        switch_mac={}
        print(type(type(item.name)))
        print(item.name)
        neighbors[item.name]=list_switch
        mac[item.name]=switch_mac
    dic_temp={}
    mac_all={}
    for item in net.links:
        count1=item.intf1.name.find('-')
        count2=item.intf2.name.find('-')
        print(item.intf1.name[:count1])
        print(item.intf2.name[:count2])
        if item.intf1.name not in dic_temp:
            dic_temp[item.intf1.name]=1
        if item .intf2.name not in dic_temp:
            dic_temp[item.intf2.name]=1
        node1=item.intf1.name[:count1]
        node2=item.intf2.name[:count2]
        neighbors[node1].append(node2)
        neighbors[node2].append(node1)
        mac[node1][node2]=item.intf1.mac
        mac[node2][node1]=item.intf2.mac
        mac_all[item.intf1.name]=item.intf1.mac
        mac_all[item.intf2.name]=item.intf2.mac
        print(item.intf1.mac)
        print(item.intf2.mac)
        print(type(item.intf1.mac))
        print(type(item.intf2.mac))
    f_mac_all=open("mac_all.txt",'w')

    for item in mac_all:
        f_mac_all.write(item+'\t'+mac_all[item]+'\t'+'\n')

    for item in neighbors:
        print(item+'\t')
        for temp in neighbors[item]:
            print(temp+'\t')
            f_neighbors.write(item+'\t'+temp+'\n')
        print('\n')
    for item in mac:
        print(item+'\t')
        for temp in mac[item]:
            print(temp+'\t')
            print(mac[item][temp]+'\n')
            f_mac.write(item+'\t'+temp+'\t'+mac[item][temp]+'\n')
        print('\n')
    f_neighbors.close()
    f_mac.close()
    """
    h0=net.hosts[0]
    for item in net.hosts[1:]:
        h0.cmdPrint('ping -Q 0x64 -c 1 '+item.IP())
    """
    
    net.pingAll()
    f_temp=open('tcplook.sh','w')
    for item in dic_temp:
        f_temp.write('sudo tcpdump -i '+item+' -w '+item+'.pcap'+' &'+'\n')
    f_temp.close()
    global tcp_start
    tcp_start=time.time()
    os.system('sh -x tcplook.sh')
    #sleep(2)
    samples=1

    
    for i in range(samples):
        print(i)
        #event=random.randint(0,2)
        event=0
        h0=net.hosts[0]
        h1=net.hosts[1]
        h2=net.hosts[2]
        #h0.cmdPrint('ping -Q 0x64 -c 1 '+h1.IP())
        #sleep(3)
        if(event==0):
            #normal(net,i)
            traffic(net,i)
        if(event==1):
            brokenlink(net,i)
        if(event==2):
            brokenswitch(net,i,brokennode)
        sleep(1)
    net.stop()
if __name__ == "__main__":
    print("GO")
    myNet()
# topos = { 'generated': ( lambda: GeneratedTopo() ) }
