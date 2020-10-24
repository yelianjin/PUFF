# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 23:37:13 2020

@author: Administrator
"""
import networkx as nx
import matplotlib.pyplot as plt
import sys
f=open('1221_latencies.intra','r')

node={}
link={}

for line in f:
    print(line)
    keys=line.split(' ')
    keys[2]=keys[2].strip()
    s1='b'+keys[0][-4:]
    s2='b'+keys[1][-4:]
    l=s1+'+'+s2
    if s1 not in node:
        node[s1]=len(node)
    if s2 not in node:
        node[s2]=len(node)
    if l not in link:
        link[l]=keys[2]

f.close()

nodes=[]
edges=[]
error=[89,90,14,13]
for n in node:
    if node[n] in error:
        continue
    nodes.append(str(node[n]))

print(nodes)
for l in link:
    n=l.split('+')
    e1=node[n[0]]
    e2=node[n[1]]
    if e1 in error or e2 in error:
        continue
    key=(str(e1),str(e2))
    edges.append(key)

print(edges)

G=nx.Graph()
# G=nx.DiGraph()

for a in nodes:
    G.add_node(a)

r=G.add_edges_from(edges)
nx.draw(G, node_size=1,font_size=9,with_labels=True,node_color='y',)
plt.show()




