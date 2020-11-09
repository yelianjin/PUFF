# -*- coding: utf-8 -*-
import time
import sys
import sched
import numpy as np
class PPBP():
    def __init__(self):
        ##10Mbps
        ##unit:bit
        self.m_cbrRate=100*1024*1024
        self.m_pktSize=1470
        self.m_burstArrivals=float(50)
        self.m_burstlength=float(0.5)
        self.m_h=float(0.7)
        self.m_totalBytes=0
        self.m_activebursts=0
        self.m_offPeriod=True
        self.lastStartTime=time.time()
        self.initialTime=self.lastStartTime
        self.flowSize=1024*8
        self.s=sched.scheduler(time.time,time.sleep)
        self.count_all=int(self.flowSize/1448)
        self.exp_set=np.random.exponential(float(1/self.m_burstArrivals),1024)
        self.count=0
        self.m_shape=3-2*self.m_h
        self.t_pareto_set=np.random.pareto(self.m_shape,1024)*self.m_burstlength
        ##No mtxTrace()
        
    def process(self):
        if (self.m_totalBytes>=self.flowSize):
            sys.exit(0)
        t_poisson_arrival=self.exp_set[self.count]
		#m_PoissonArrival =s.enter(t_poisson_arrival,1,self.PoissonArrival);

        self.s.enter(self.lastStartTime-self.initialTime+t_poisson_arrival,1,self.PoissonArrival)
		#m_timeSlot=(self.m_shape - 1) * self.m_burstLength /self.m_shape

        ###a:scale
        ###shape: shape
        #t_pareto=np.random.pareto(m_shape,1)*self.m_burstlength
        t_pareto=self.t_pareto_set[self.count]
        self.s.enter(self.lastStartTime-self.initialTime+t_poisson_arrival+t_pareto,1,self.ParetoDeParture)
        self.s.enter(self.lastStartTime-self.initialTime+t_poisson_arrival,1,self.process)
        self.count+=1
        if (self.m_totalBytes>=self.flowSize):
            sys.exit(0)


    def PoissonArrival(self):
         self.m_activebursts+=1
         if(self.m_offPeriod):
             self.ScheduleNextTx()
    
    
    def ParetoDeParture(self):
        self.m_activebursts-=1
        
    def ScheduleNextTx(self):
         
        ##Schedule Next burst 
        bits = (self.m_pktSize + 30) * 8;
        nextTime=float(bits/self.m_cbrRate)
        #if(self.m_activebursts != 0)
        if (self.m_activebursts!=0 and self.m_totalBytes<=self.flowSize):
            print('HI')
            self.m_offPeriod = False
            data_rate=nextTime/self.m_activebursts
            self.m_lastStartTime=time.time()
            self.s.enter(self.m_lastStartTime-self.initialTime+data_rate,1,self.send_packet)
            print('TEST')
            self.m_totalBytes+=1448
            print(self.m_totalBytes)
        elif(self.m_activebursts==0):
            self.m_offPeriod = True
        elif(self.m_totalBytes>self.flowSize):
            sys.exit(0)

    
    def send_packet(self):
        self.ScheduleNextTx()
        #s1()
        #print('1470')
        #print(self.m_lastStartTime)
   
def s1():
    print(time.time()-start)
    print('GO')

if __name__=="__main__":
    start=time.time()
    b=PPBP()

    """
    s=sched.scheduler(time.time,time.sleep)
    s.enter(1,1,print_time,kwargs={'a':'1'})
    s.enter(1,1,print_time,kwargs={'a':'2'})
    print(time.time())
    s.run()
    print(time.time())
    """
    b.process()
    print(b.t_pareto_set)
    print(b.exp_set)
    print('initial')
    print(time.time()-start)
    c=b.s
    try:
        c.run()
    except:
        print('OK')
    print('A')
    print(time.time()-start)
    #print('end')
    #print(time.time()-start)