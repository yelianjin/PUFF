# -*- coding: utf-8 -*-
import time
import sys
from threading import Timer
import socket
import random
class PPBP():
    def __init__(self,size,e1,t):
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
        self.flowSize=size
        self.T=None
        self.e=e1.split('+')
        self.count_arrive=0
        self.count_departure=0
        self.m_shape=3-2*self.m_h
        self.p=t.split('+')
        self.exp_set=None
        self.t_pareto_set=None
        ##No mtxTrace()
    
    def set(self):
        l1=[]
        for i in self.e:
            l1.append(float(i))
        l2=[]
        for i in self.p:
            l2.append(float(i))
        self.exp_set=l1
        self.t_pareto_set=l2

    def process(self):
        if(self.flowSize<=1448):
            self.send_packet(str(self.flowSize))

        if (self.m_totalBytes>=self.flowSize):
            #print('HEY1')
            sys.exit(0)
        #t_poisson_arrival=self.exp_set[count1]
        #t_poisson_arrival=0.01


        ##test of sched
        ##seems no sched in HOST
        
        ##test of Timer
        ##timer is OK
        """
        for i in range(4):
            timer=Timer(0.01, self.send_packet,('1448',))
            timer.start()
        """ 
        count1=1
        count2=1
        t_poisson_arrival=self.exp_set[count1]
        t_pareto=self.t_pareto_set[count2]
        print(t_poisson_arrival)
        print(t_pareto)
        timer1=Timer(t_poisson_arrival,self.PoissonArrival)
        timer2=Timer(t_poisson_arrival+t_pareto,self.ParetoDeParture)
        timer3=Timer(t_poisson_arrival,self.process)
        if(self.m_totalBytes>=size):
            sys.exit(0)
        
        timer1.start()
        timer2.start()
        timer3.start()
    
        #t_poisson_arrival=(np.random.exponential(float(1/self.m_burstArrivals),1))[0]
		#m_PoissonArrival =s.enter(t_poisson_arrival,1,self.PoissonArrival);

        #self.s.enter(self.lastStartTime-self.initialTime+t_poisson_arrival,1,self.PoissonArrival)
		#m_timeSlot=(self.m_shape - 1) * self.m_burstLength /self.m_shape
        #self.s.enter(t_poisson_arrival,1,self.PoissonArrival)
        ###a:scale
        ###shape: shape
        #t_pareto=(np.random.pareto(self.m_shape,1)*self.m_burstlength)[0]
        #count2=random.randint(0,255)
        #t_pareto=self.t_pareto_set[count2]
        #self.s.enter(self.lastStartTime-self.initialTime+t_poisson_arrival+t_pareto,1,self.ParetoDeParture)
        #self.s.enter(self.lastStartTime-self.initialTime+t_poisson_arrival,1,self.process)
        #self.s.enter(t_poisson_arrival+t_pareto,1,self.ParetoDeParture)
        #self.s.enter(t_poisson_arrival,1,self.process)
        if (self.m_totalBytes>=self.flowSize):
            #print('HEY2')
            sys.exit(0)
    
        
    def PoissonArrival(self):
         self.m_activebursts+=1
         print(self.m_activebursts)
         self.count_arrive+=1
         print(self.m_offPeriod)
         if(self.m_offPeriod):
             self.ScheduleNextTx()
    
    
    def ParetoDeParture(self):
        print(self.count_departure)
        self.count_departure+=1
        self.m_activebursts-=1
    
    def ScheduleNextTx(self):
        print('test')     
        ##Schedule Next burst 
        bits = (self.m_pktSize + 30) * 8;
        nextTime=float(bits/self.m_cbrRate)
        #if(self.m_activebursts != 0)
        if (self.m_activebursts!=0 and self.m_totalBytes<=(self.flowSize-1448)):
            self.m_offPeriod = False
            data_rate=nextTime/self.m_activebursts
            #self.m_lastStartTime=time.time()
            #self.s.enter(self.m_lastStartTime-self.initialTime+data_rate,1,self.send_packet)
            timer4=Timer(data_rate,self.send_packet,('1448',))
            timer4.start()
            #self.m_totalBytes+=1448
            #print(self.m_totalBytes)
        elif(self.m_activebursts==0):
            self.m_offPeriod = True
        elif(self.m_activebursts!=0 and self.m_totalBytes>=(self.flowSize-1448)):
            data_rate=nextTime/self.m_activebursts
            timer5=Timer(data_rate,self.send_packet,(str(self.flowSize-self.m_totalBytes),))
            timer5.start()
            #print('HEY4')
            #self.m_totalBytes=self.flowSize
            #sys.exit(0)
        elif(self.m_totalBytes>self.flowSize):
            #print('HEY3')
            sys.exit(0)

    def send_packet(self,temp_size):
        #print(temp_size)
        so.send(P1[:int(temp_size)].encode())
        self.m_totalBytes+=int(temp_size)
        print(temp_size)
        sys.exit(0)
        #print(self.m_totalBytes)
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
def test():
    P2=''
    for i in range(4344):
        P2+='b'
    so.sendall(P2.encode())
    so.close()
    sys.exit(0)

def changeoff():
    global m_activebursts
    m_activebursts-=1


if __name__=="__main__":
    global so
    ip_source=sys.argv[1]
    ip_dst=sys.argv[2]
    port_dst=10000+int(sys.argv[6])
    addr=(ip_dst,port_dst)
    size=int(sys.argv[3])
    exp=sys.argv[4]
    pareto=sys.argv[5]
    print(exp)
    print(pareto)
    so=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('TEST')
    so.connect(addr)
    #start=time.time()
    print('HI0')
    global b
    b=PPBP(size,exp,pareto)
    print('HI')
    b.set()

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
    #b.process()
    #print(b.t_pareto_set)
    #print(b.exp_set)
    #print('initial')
    #start1=time.time()
    #print(start1-start)
    print('HI')
    
    #b.process()
    totalBytes=0
    m_activebursts=0
    global m_offPeriod
    m_offPeriod=True
    global count_arrive
    count_arrive=0
    global count_departure
    count_departure=0

    while(totalBytes<=size):
        ##Arrival
        ##ScheduleNextTx
        
        count1=random.randint(0,255)
        count2=random.randint(0,255)
        time.sleep(b.exp_set[count1])
        a=Timer(b.t_pareto_set[count2],changeoff)
        a.start()
        if(size<=1448):
            so.send(P1[:size].encode())
            break
        else:
            m_activebursts+=1
            if(m_offPeriod==False):
                if(m_activebursts!=0):
                    m_offPeriod=True
                    print('I have changed')
                continue
            if(m_activebursts!=0):
                m_offPeriod=False
                so.send(P1.encode())
                totalBytes+=1448
                print('AAA')
            else:
                m_offPeriod=True
            

    so.send('quit'.encode())
    so.close()
    print(totalBytes)
