# -*- coding:UTF-8 -*-
import sys
####只汇报点的问题
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

def greedy():
    dic_choice={}
    switch_all={}
    cost={}
    ###最大覆盖问题的贪心近似解
    ###这里是做到了选入点的收益为1的时候停掉
    ###while(nodes)情况为全部都在一跳邻居范围内的点
    ###finalnode是最终结果,set
    nodes=set()
    for i in range(count_brokennode+1):
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

def bfs():
    ###由于这里是无向连通图，这里相当于对邻居BFS就可以得到邻居的最短路距离
    ###distance_all distance_all[start_node][i]为start_node到i的最短路距离,type 为int
    ###short_all  short_all[start_node][i]为start_node到i的最短路List,type为list e.g short_all[s1][s3]=[s1,s2,s3]
    ###appear_all appear_all[start_node]
    ###distance_all={}
    short_all={}
    appear_all={}
    for i in range(count_brokennode+1):
        ###初始化
        start_node='s'+str(i)
        distance={}
        short={}
        appear={}
        nodes=set()
        ###初始化nodes集,appear数
        for j in range(count_brokennode+1):
            nodes.add('s'+str(j))
            appear['s'+str(j)]=0

        ###初始化short_list
        for j in range(count_brokennode+1):
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
            for j in range(count_brokennode+1):
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
    for i in range(count_brokennode+1):
        key='s'+str(i)
        exist_all[key]=0
    for i in range(count_brokennode+1):
        key='s'+str(i)
        for j in range(count_brokennode+1):
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
    for i in range(count_brokennode+1):
        node='s'+str(i)
        temp={}
        for j in final_node:
            temp[j]=distance_all[node][j]
        result=sorted(temp.items(),key=lambda x:x[1])
        distance_choice[node]=result
    
    ###根据ip取特征的过程，获得所有Link
    link_switch=dic
    for i in range(count_brokennode+1):
        link_switch['s'+str(i)].remove('s'+str(i))

    ###根据ip取特征的过程，获得所有node
    node_all={}
    for i in range(count_brokennode+1):
        key1='s'+str(i)
        node_all[key1]=[]

    ###读文件
    for i in range(event+1):
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
        window_count=4
        for k in range(window_count):
            fs={}
            for j in final_node:
                fs[j]=open(path1+j+'-'+str(k)+'_1.txt','r').readlines()
            
        ###数据包特征化

            for item in node_all:
                key1=item
                s1=key1[1:]
                count1=int(s1)        
                for switch in distance_choice[key1]:
                    #if switch[0]==key1:
                        #continue
                    info=fs[switch[0]][count1]
                    infos=info.split('\t')
                    for k in range(2,14):
                        node_all[item].append(infos[k].strip())
                
                ###以下为邻居信息的获得
                for switch in distance_choice[key1]:
                    #if switch[0]==key1:
                        #continue
                    ##count_temp1:f1的计算
                    ##count_temp2:f2的计算
                    ##count_temp3:f3的计算
                    ##count_temp4:f4的计算
                    ##count_temp5:总共的一跳邻居数
                    ##count_temp6:f5的计算
                    ##count_temp7:f6的计算
                    ##           :f12的计算
                    count_temp1=0
                    count_temp2=0
                    count_temp3=0
                    count_temp4=0
                    count_temp5=0
                    count_temp6=0
                    count_temp7=0
                    count_temp8=0
                    count_temp9=0
                    count_temp10=0
                    count_temp11=0
                    count_temp12=0
                    count_temp13=0
                    count_temp14=0
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
                        count_temp6+=float(infos[6].strip())
                        count_temp7+=float(infos[7].strip())
                        count_temp8+=float(infos[8].strip())
                        count_temp9+=float(infos[9].strip())
                        count_temp10+=float(infos[10].strip())
                        count_temp11+=float(infos[11].strip())
                        count_temp12+=float(infos[12].strip())
                        count_temp13+=float(infos[13].strip())
                    result1=float(count_temp1/count_temp5)
                    result2=float(count_temp2/count_temp5)
                    result3=float(count_temp3/count_temp5)
                    result4=float(count_temp4/count_temp5)
                    result5=float(count_temp6/count_temp5)
                    result6=float(count_temp7/count_temp5)
                    result7=float(count_temp8/count_temp5)
                    result8=float(count_temp9/count_temp5)
                    result9=float(count_temp10/count_temp5)
                    result10=float(count_temp11/count_temp5)
                    result11=float(count_temp12/count_temp5)
                    result12=float(count_temp13/count_temp5)
                    node_all[item].append(str(result1))
                    node_all[item].append(str(result2))
                    node_all[item].append(str(result3))
                    node_all[item].append(str(result4))
                    node_all[item].append(str(result5))
                    node_all[item].append(str(result6))
                    node_all[item].append(str(result7))
                    node_all[item].append(str(result8))
                    node_all[item].append(str(result9))
                    node_all[item].append(str(result10))
                    node_all[item].append(str(result11))
                    node_all[item].append(str(result12))






            




            ###标注node_all的正负样本标注
        for item in node_all:

            s1=item[1:]
            count1=int(s1) 
            if count1==i :
                node_all[item].append(str(1))
            else:
                node_all[item].append(str(0))

        print(len(node_all[item]))

    ###写文件
        fdata=open(path1+'data.txt','w')
        for item1 in node_all:
            fdata.write('brokennode'+str(i)+item1+'\t')
            for item2 in node_all[item1]:
                fdata.write(item2+'\t')
            fdata.write('\n')
        fdata.close()

    ###清空列表
        for item1 in node_all:
            del node_all[item1][:]


if __name__=='__main__':
##count_brokennode brokennode文件夹数量
##count_monitor检测节点数量
    global count_brokennode
    count_brokennode=41
    global event
    event=41
    global count_monitor
    count_monitor=int(sys.argv[1])
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
    print(final_node)
    factorization(final_node)
