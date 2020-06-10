# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 23:37:13 2020

@author: Administrator
"""

import sys
f=open('1221_latencies.intra','r')
f_result=open('1221.py','w')
node={}
link={}

for line in f:
    print(line)
    keys=line.split(' ')
    keys[2]=keys[2].strip()
    s1=keys[0][-4:]
    s2=keys[1][-4:]
    l=s1+'+'+s2
    if s1 not in node:
        node[s1]=len(node)
    if s2 not in node:
        node[s2]=len(node)
    if l not in link:
        link[l]=keys[2]

f.close()
print(node)
print(link)


for i in node:
    temp=i+' = self.addSwitch( \'s'+str(node[i])+'\',failMode=\'standalone\',stp=True)\n'
    f_result.write(temp)
for i in range(3):
    f_result.write('\n')

for i in node:
    temp=i+'_host = self.addHost( \'h'+str(node[i])+'\',ip=\'192.168.123.'+str(node[i]+1)+'\')\n'
    f_result.write(temp)
for i in range(3):
    f_result.write('\n')
    
for i in node:
    temp='self.addLink( '+i+' , '+i+'_host )\n'
    f_result.write(temp)
for i in range(3):
    f_result.write('\n')
    
for i in link:
    keys=i.split('+')
    e1=keys[0]
    e2=keys[1]
    d=link[i]
    temp='self.addLink( '+e1+' , '+e2+', bw=10, delay=\''+d+'ms\')\n'
    f_result.write(temp)
f_result.close()