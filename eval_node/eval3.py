# -*- coding:UTF-8 -*-
import sys

def initialize():
###从neighbors.txt中读取是路由器两端的链路
###dic['s0']保存s0周围的邻居

    link=open('neighbors.txt','r')
    count_link=0
    for i in range(count_brokennode+1):
        link1=set()
        dic['s'+str(i)]=link1
    ###加入链路
    for links in link:
        keys=links.split('\t')
        host1=keys[0].strip()
        host2=keys[1].strip()
        if host1[0]=='s' and host2[0]=='s':
            if host1 not in dic[host2]:
                dic[host2].add(host1)
            if host2 not in dic[host1]:
                dic[host1].add(host2)
            count_link+=1
    print(count_link)

    for item in dic:
        print (item+'\t')
        dic[item].add(item)
        for temp in dic[item]:
            print(temp+'\t')
        print('\n')
    count=2
    max=0

def greedy(count_monitor):
    dic_choice={}
    switch_all={}
    cost={}
    ###最大覆盖问题的贪心近似解
    ###这里是做到了选入点的收益为1的时候停掉
    ###while(nodes)情况为全部都在一跳邻居范围内的点
    ###finalnode是最终结果,set
    nodes=set()
    for i in range(40):
        nodes.add('s'+str(i))
    final_node=set()
    print(len(nodes))
    k=2
    for i in range(count_monitor):
    #while (nodes):
        best_node=None
        node_covered=set()
        for node in dic:
            if node in final_node:
                continue
            else:
                covered=nodes & dic[node]
                if len(covered) >len(node_covered):
                    best_node=node
                    node_covered=covered
        nodes-=node_covered
        final_node.add(best_node)
        print(len(nodes))
    print(final_node)
    return final_node

def bfs():
    ###由于这里是无向连通图，这里相当于对邻居BFS就可以得到邻居的最短路距离
    ###distance_all distance_all[start_node][i]为start_node到i的最短路距离,type 为int
    ###short_all  short_all[start_node][i]为start_node到i的最短路List,type为list e.g short_all[s1][s3]=[s1,s2,s3]
    ###appear_all appear_all[start_node]
    ###distance_all={}
    short_all={}
    appear_all={}
    for i in range(40):
        ###初始化
        start_node='s'+str(i)
        distance={}
        short={}
        appear={}
        nodes=set()
        ###初始化nodes集,appear数
        for j in range(40):
            nodes.add('s'+str(j))
            appear['s'+str(j)]=0

        ###初始化short_list
        for j in range(40):
            temp_list=[]
            temp_list.append(start_node)
            short['s'+str(j)]=temp_list
            #short_all[start_node]=short['s'+str(j)]
        count=1
        
        ###初始化distance距离,neighbors是已覆盖的集合
        distance[start_node]=0
        short_all[start_node]=short

        
        neighbors=set()
     

        before={}
        before[start_node]=start_node
        ###初始化起始点的1跳,和1跳邻居的前项
        for item in dic[start_node]:
            neighbors.add(item)
            before[item]=start_node

        while nodes:
            nodes-=neighbors
            temp=set()
            print(count)
            for item in neighbors:
                if item not in distance:
                    distance[item]=count
                    ###Python的a=b是指向同一地址，所以要[:]
                    short[item]=short[before[item]][:]
                    print(short[item])
                    short[item].append(item)
                    print(short[item])
                for j in dic[item]:
                    temp.add(j)
                    if (j not in neighbors) and (j not in distance):
                        before[j]=item
            print(len(distance))

            neighbors=neighbors | temp
            count+=1

        distance_all[start_node]=distance
        short_all[start_node]=short
        for item in short:
            short_all[start_node][item]=short[item]
        
        ###测试用
        """
        for item in short:
            print(item)
            print(short[item])
        """
        ###做appear计算
        ###appear[key]计算的是key在start_node确定时作为最短路径中一部分的次数
        for item in short:
            for j in range(40):
                key='s'+str(j)
                if(key in short_all[start_node][item]):
                    appear[key]+=1
        
        appear_all[start_node]=appear
        for item in appear_all[start_node]:
            print(item)
            print(appear_all[start_node][item])
        
    ###计算所有点作为最短路径中一点的次数
    ###exist_all[key],key作为最短路径中一点的次数
    exist_all={}
    for i in range(40):
        key='s'+str(i)
        exist_all[key]=0
    for i in range(40):
        key='s'+str(i)
        for j in range(40):
            start_node='s'+str(j)
            exist_all[key]+=appear_all[start_node][key]
    result=sorted(exist_all.items(),key=lambda x:x[1],reverse=True)
    ###result是以在最短路径中出现次数进行从大到小排序的tuple
    ###result[0][1]取出最多的点的次数
    return result

def factorization(final_node):
    ###按与监控点的最近邻距离进行顺序排序，distance_choice为dic，其中放了List
    ###distance_all['s0']是s0与选中点的最短跳数
    ###distance_all['s0']第k项的[0]是第K个最近选中点
    ###distance_all['s0']第k项的[1]是s0与第K个最近选中点的跳数
    distance_choice={}
    for i in range(40):
        node='s'+str(i)
        temp={}
        for j in final_node:
            temp[j]=distance_all[node][j]
        result=sorted(temp.items(),key=lambda x:x[1])
        distance_choice[node]=result
    
    ##test_print
    for i in range(40):
        print(i)
        print(distance_choice['s'+str(i)])

    
    ###根据ip取特征的过程，获得所有Link
    link_switch=dic
    for i in range(40):
        link_switch['s'+str(i)].remove('s'+str(i))
    link_all={}
    for i in range(40):
        for j in link_switch['s'+str(i)]:
            key1='s'+str(i)+'+'+j
            key2=j+'+'+'s'+str(i)
            if key1 not in link_all and key2 not in link_all:
                a=[]
                link_all[key1]=a
    ###读文件
    for i in range(count_brokennode+1):
    ###开始读写
        path1='brokennode'+str(i)+'/'
    ###假定观测节点不会down掉
        judge='s'+str(i)
        if judge in final_node:
            fdata=open(path1+'data.txt','w')
            fdata.write('\n')
            fdata.close()
            continue
    ###开始读写
        ##count 采样窗口数量
        count=4
        for k in range(4):
            fs={}
            for j in final_node:
                fs[j]=open(path1+j+'-'+str(k)+'_1.txt','r').readlines()
            
        ###数据包特征化

            for item in link_all:
                keys=item.split('+')
                key1=keys[0].strip()
                key2=keys[1].strip()
                s1=key1[1:]
                s2=key2[1:]
                count1=int(s1)
                count2=int(s2)        
                for switch in distance_choice[key1]:
                    #if switch[0]==key1:
                        #continue
                    info=fs[switch[0]][count1]
                    infos=info.split('\t')
                    for k in range(2,6):
                        link_all[item].append(infos[k].strip())
                
            
                for switch in distance_choice[key1]:
                    #if switch[0]==key1:
                        #continue
                    count_temp1=0
                    count_temp2=0
                    count_temp3=0
                    count_temp4=0
                    count_temp5=0
                    for neighbors in dic[key1]:
                        if neighbors==key1:
                            continue
                        count_switch=int(neighbors[1:])
                        info=fs[switch[0]][count_switch]
                        infos=info.split('\t')
                        count_temp1+=float(infos[2].strip())
                        count_temp2+=float(infos[3].strip())
                        count_temp3+=float(infos[4].strip())
                        count_temp4+=float(infos[5].strip())
                        count_temp5+=1
                    result1=float(count_temp1/count_temp5)
                    result2=float(count_temp2/count_temp5)
                    result3=float(count_temp3/count_temp5)
                    result4=float(count_temp4/count_temp5)
                    link_all[item].append(str(result1))
                    link_all[item].append(str(result2))
                    link_all[item].append(str(result3))
                    link_all[item].append(str(result4))
            
                for switch in distance_choice[key2]:
                    #if switch[0]==key2:
                        #continue
                    info=fs[switch[0]][count2]
                    infos=info.split('\t')
                    for k in range(2,6):
                        link_all[item].append(infos[k].strip())
                
                for switch in distance_choice[key2]:
                    #if switch[0]==key2:
                        #continue
                    count_temp1=0
                    count_temp2=0
                    count_temp3=0
                    count_temp4=0
                    count_temp5=0
                    for neighbors in dic[key2]:
                        if neighbors==key2:
                            continue
                        count_switch=int(neighbors[1:])
                        info=fs[switch[0]][count_switch]
                        infos=info.split('\t')
                        count_temp1+=float(infos[2].strip())
                        count_temp2+=float(infos[3].strip())
                        count_temp3+=float(infos[4].strip())
                        count_temp4+=float(infos[5].strip())
                        count_temp5+=1
                    result1=float(count_temp1/count_temp5)
                    result2=float(count_temp2/count_temp5)
                    result3=float(count_temp3/count_temp5)
                    result4=float(count_temp4/count_temp5)
                    link_all[item].append(str(result1))
                    link_all[item].append(str(result2))
                    link_all[item].append(str(result3))
                    link_all[item].append(str(result4))
            



            ###标注Link_all的正负样本标注
        for item in link_all:
            keys=item.split('+')
            key1=keys[0].strip()
            key2=keys[1].strip()
            s1=key1[1:]
            s2=key2[1:]
            count1=int(s1)
            count2=int(s2) 
            if count1==i or count2==i:
                link_all[item].append(str(1))
            else:
                link_all[item].append(str(0))

        print(len(link_all[item]))

    ###写文件
        fdata=open(path1+'data.txt','w')
        for item1 in link_all:
            fdata.write('brokennode'+str(i)+item1+'\t')
            for item2 in link_all[item1]:
                fdata.write(item2+'\t')
            fdata.write('\n')
        fdata.close()

    ###清空列表
        for item1 in link_all:
            del link_all[item1][:]

def count_flow(nodelist):
    flow_all={}
    path1="/home/ylj/GEANT/ev/brokennode0/"
    for i in nodelist:
        path2=path1+i+'.txt'
        f=open(path2,'r')
        for item in f:
            keys=item.split('\t')
            src=keys[1]
            dst=keys[3]
            protocol=keys[4]
            temp=src+dst
            if(protocol=='TCP' and temp not in flow_all):
                flow_all[temp]=1
    return flow_all

if __name__=='__main__':
##count_brokennode brokennode文件夹数量
##count_monitor检测节点数量
    global count_brokennode
    count_brokennode=39
    global count_monitor
    count_monitor=4
    global dic
    dic={}
    initialize()
    global distance_all
    distance_all={}
    bfs_result=bfs()
    print(bfs_result)
    final_node=[]
    for i in range(count_monitor):
        final_node.append(bfs_result[i][0])
    print("shortest path")
    print(final_node)
    greedy_result=greedy(count_monitor)
    print("Greed point")
    print(greedy_result)
    #factorization(final_node)
    print(type(final_node))
    print(type(greedy_result))

    #count_flow
    ##flow_all
    node_all=[]
    for i in range(count_brokennode+1):
        node_all.append('s'+str(i))
    flow_all=count_flow(node_all)
    flow_greedy=count_flow(greedy_result)
    flow_shortest=count_flow(final_node)
    print(len(flow_all))
    print(len(flow_greedy))
    print(len(flow_shortest))
