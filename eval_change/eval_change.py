# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 20:26:21 2020

@author: think
"""
import numpy as np
import sys
def get_feature(switch_count):
    
    ##假设为30维，[0,15)为一端,[15.30)为另一端
    feature=8
    ##这里的问题是总共的维度是512维。512维的含义是 4*128
    ##time_epoch的意思是有4个时间切片
    ##这里的含义是[0:2)是数据包数量.[2,4)是重发包数量，[0,32)是自己的信息，[32,64]是邻居的信息
    ##epoch是每个的起点
    epoch=8
    sample_epoch=384
    ##这里epoch是4（个特征）*2(邻居信息)*8(个swithc_count)

    ##没有重发包的版本
    f1={}
    f2={}
    for e in range(epoch):
        f1[e]={}
        f2[e]={}
        for s in range(0,switch_count):
            f1[e][s]={}
            f2[e][s]={}

    for e in range(epoch):
        base1=e*sample_epoch
        base2=e*sample_epoch+192
        for s in range(0,switch_count):
            for f in [0,1,4,5,6,7,8,9,10,11]:
            #for f in [0,1,4,5]:
                query1=base1+s*12+f
                query2=base2+s*12+f
                #query3=query1+96
                #query4=query2+96
                f1[e][s][f]=query1
                f2[e][s][f]=query2
                
                #feature_list.append(query3)
                #feature_list.append(query4)
                
    return f1,f2
        
def analysis(path,feature_list,target):
    
    ##加载数据
    ##对于x来说
    ##在一条链路两端  [0:15) 是h0的 5个观测点的3个有关特征 维度是3*5
    ##[15:30)是h1 的5个观测点的3个有关特征 维度是3*5
    

    #path:  测试集路径
    #feature_list:  向量集特征
    #target:    预测的维度
    data=np.loadtxt(path,usecols=np.arange(1,target+2))
    X=data[:,feature_list]
    y=data[:,target]
    
    
    f=open(path,'r')
    r=f.readlines()
    l=[]
    for line in r:
        info=1
        keys=line.split(' ')
        temp=keys[0]
        count_s=temp.find('s')
        snap=temp[len('brokennode'):count_s]
        add=temp.find('+',count_s)
        end1=temp[count_s+1:add]
        end2=temp[add+2:]
        if (end1==snap):
            info=1
        else:
            info=2
        l.append(info)
    
    l=np.array(l)
    X=np.column_stack((X,l))
    
    
    ##拼接是否是brokennode的点
    arr1=X[X[:,384*8]==1,:]
    arr2=X[X[:,384*8]==2,:]
    
    ##是brokennode的情况
    return arr1,arr2
    
def query(feature1,feature2):
    epoch=8
    sample_epoch=384
    switch_count=8
    q1=[]
    q2=[]
    for e in range(epoch):
        for s in range(1,2):
            q1.append(feature1[e][s][7])
    for e in range(epoch):
        for s in range(1,2):
            q2.append(feature2[e][s][7])
    
    broke=np.vstack((a1[:,q1],a2[:,q2]))
    normal=np.vstack((a1[:,q2],a2[:,q1]))
    
    print(broke.shape)
    print(normal.shape)
    return broke,normal

def trend(b,r):
    b_t=np.mean(b,axis=0)
    r_t=np.mean(r,axis=0)
    return b_t,r_t
    
def process(path):
    f=open(path+'.txt','r')
    r=f.readlines()
    f0=open(path+'_0.txt','w')
    f1=open(path+'_1.txt','w')
    for line in r:
        keys=line.split(' ')
        if keys[-1].strip()=='1':
            f1.write(line)
        else:
            f0.write(line)
    f0.close()
    f1.close()
    f.close()
    
if __name__ =="__main__":
    #path='chinaNet_link_46_8_b'
    #process(path)
    
    path='chinaNet_link_46_8_b_1.txt'
    
    target=384*8
    global feature1,feature2
    feature1,feature2=get_feature(8)
    
    print(feature1)
    print(feature2)
    global a1,a2
    a1,a2=analysis(path,[i for i in range(384*8)],target)
    b,r=query(feature1,feature2)
    b_t,r_t=trend(b,r)
    print(b_t)
    print(r_t)