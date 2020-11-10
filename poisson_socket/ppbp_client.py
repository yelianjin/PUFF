# -*- coding: utf-8 -*-
import time
import sys
import sched
import numpy as np
import socket

class PPBP():
    def __init__(self,size):
        ##10Mbps
        ##unit:bit
        self.m_cbrRate=100*1024*1024
        self.m_pktSize=1470
        self.m_burstArrivals=float(5)
        self.m_burstlength=float(0.05)
        self.m_h=float(0.7)
        self.m_totalBytes=0
        self.m_activebursts=0
        self.m_offPeriod=True
        self.lastStartTime=time.time()
        self.initialTime=self.lastStartTime
        self.flowSize=size
        self.s=sched.scheduler(time.time,time.sleep)
        self.exp_set=np.random.exponential(float(1/self.m_burstArrivals),1024)
        self.count=0
        self.count_arrive=0
        self.count_departure=0
        self.m_shape=3-2*self.m_h
        self.t_pareto_set=np.random.pareto(self.m_shape,1024)*self.m_burstlength
        ##No mtxTrace()
        
    def process(self):
        if(self.flowSize<=1448):
            self.send_packet(str(self.flowSize))
            sys.exit(0)
        if (self.m_totalBytes>=self.flowSize):
            print('HEY1')
            sys.exit(0)
        print('HI')
        t_poisson_arrival=self.exp_set[self.count]
        #t_poisson_arrival=(np.random.exponential(float(1/self.m_burstArrivals),1))[0]
		#m_PoissonArrival =s.enter(t_poisson_arrival,1,self.PoissonArrival);

        #self.s.enter(self.lastStartTime-self.initialTime+t_poisson_arrival,1,self.PoissonArrival)
		#m_timeSlot=(self.m_shape - 1) * self.m_burstLength /self.m_shape
        self.s.enter(t_poisson_arrival,1,self.PoissonArrival)
        ###a:scale
        ###shape: shape
        #t_pareto=(np.random.pareto(self.m_shape,1)*self.m_burstlength)[0]
        t_pareto=self.t_pareto_set[self.count]
        #self.s.enter(self.lastStartTime-self.initialTime+t_poisson_arrival+t_pareto,1,self.ParetoDeParture)
        #self.s.enter(self.lastStartTime-self.initialTime+t_poisson_arrival,1,self.process)
        self.s.enter(t_poisson_arrival+t_pareto,1,self.ParetoDeParture)
        self.s.enter(t_poisson_arrival,1,self.process)
        self.count+=1
        if(self.count>=1024):
            self.count=0
        if (self.m_totalBytes>=self.flowSize):
            print('HEY2')
            sys.exit(0)


    def PoissonArrival(self):
         self.m_activebursts+=1
         self.count_arrive+=1
         if(self.m_offPeriod):
             self.ScheduleNextTx()
    
    
    def ParetoDeParture(self):
        self.count_departure+=1
        self.m_activebursts-=1
    
    def ScheduleNextTx(self):
         
        ##Schedule Next burst 
        bits = (self.m_pktSize + 30) * 8;
        nextTime=float(bits/self.m_cbrRate)
        #if(self.m_activebursts != 0)
        if (self.m_activebursts!=0 and self.m_totalBytes<=(self.flowSize-1448)):
            self.m_offPeriod = False
            data_rate=nextTime/self.m_activebursts
            #self.m_lastStartTime=time.time()
            #self.s.enter(self.m_lastStartTime-self.initialTime+data_rate,1,self.send_packet)
            self.s.enter(data_rate,1,self.send_packet,kwargs={'temp_size':'1448'})
            #self.m_totalBytes+=1448
            #print(self.m_totalBytes)
        elif(self.m_activebursts==0):
            self.m_offPeriod = True
        elif(self.m_activebursts!=0 and self.m_totalBytes>=(self.flowSize-1448)):
            data_rate=nextTime/self.m_activebursts
            self.s.enter(data_rate,1,self.send_packet,kwargs={'temp_size':str(self.flowSize-self.m_totalBytes)})
            print('HEY4')
            #self.m_totalBytes=self.flowSize
            #sys.exit(0)
        elif(self.m_totalBytes>self.flowSize):
            print('HEY3')
            sys.exit(0)

    def send_packet(self,temp_size):
        print(temp_size)
        so.send(P1[:int(temp_size)].encode())
        self.m_totalBytes+=int(temp_size)
        print(self.m_totalBytes)
        if(int(temp_size)<1448):
            sys.exit(0)
        self.ScheduleNextTx()
        #self.m_totalBytes+=temp_size
        #s1()
        #print('1470')
        #print(self.m_lastStartTime)
   
def s1():
    print(time.time()-start)
    print('GO')

if __name__=="__main__":
    global so
    os=socket.socket()
    ip_source=sys.argv[1]
    ip_dst=sys.argv[2]
    addr=(ip_dst,10000)
    size=int(sys.argv[3])
    so=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    so.connect(addr)
    start=time.time()
    b=PPBP(size)
    global P1
    P1=''
    for i in range(1448):
        P1+='b'
    """
    while(1):
        data=so.recv(1024)
        print(data)
        if data:
            break
    """
    """
    s=sched.scheduler(time.time,time.sleep)
    s.enter(1,1,print_time,kwargs={'a':'1'})
    s.enter(1,1,print_time,kwargs={'a':'2'})
    """
    b.process()
    #print(b.t_pareto_set)
    #print(b.exp_set)
    print('initial')
    start1=time.time()
    print(start1-start)
    c=b.s
    
    c.run()

    so.send('quit'.encode())
    print(time.time()-start1)
    print(b.flowSize)
    print(b.m_totalBytes)
    print(b.count_arrive)
    print(b.count_departure)
    #print('end')
    #print(time.time()-start)
