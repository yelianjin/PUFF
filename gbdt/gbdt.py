# -*- coding:UTF-8 -*-
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import svm
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
from imp import reload
from sklearn import metrics
from collections import defaultdict
import xgboost as xgb


def train(path,feature_list,target):
    
    ##加载数据
    ##对于x来说
    ##在一条链路两端  [0:15) 是h0的 5个观测点的3个有关特征 维度是3*5
    ##[15:30)是h1 的5个观测点的3个有关特征 维度是3*5
    

    #path:  测试集路径
    #feature_list:  向量集特征
    #target:    预测的维度
    data=np.loadtxt(path,usecols=np.arange(1,target+2))
    print(data.shape)
    print(data[:,target])
    print(target)

    X=data[:,feature_list]
    y=data[:,target]
    print("训练集特征")
    print(data.shape)
    print(X.shape)
    print(y.shape)

    #按3:1划分训练集和eval集
    X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=0.8,random_state=14,stratify=y)
    print("划分特征")
    print(X_train.shape)
    print(y_train.shape)
    print(X_test.shape)
    print(y_test.shape)


    #开始训练
    start=time.time()
    #n_estimators=200,learning_rate=0.5,max_depth=9
    #featyre2 n_estimators=100,learning=0.6,max_depth=5
    clf=GradientBoostingClassifier(n_estimators=200,learning_rate=0.5,max_depth=6).fit(X_train,y_train)
    #clf=svm.SVC(kernel='linear').fit(X_train,y_train)
    end=time.time()
    print("训练时间")
    print(end-start)

    #训练集上的得分
    start1=time.time()
    print("训练集得分")
    train_score=clf.score(X_train,y_train)
    print(train_score)
    print("训练集评分时间")
    print(time.time()-start1)

    #eval集上的得分
    start2=time.time()
    print(X_test.shape)
    print("eval集得分")
    eval_score=clf.score(X_test,y_test)
    print(eval_score)

    print("eval集评分时间")
    print(time.time()-start2)

    #eval集上的其他得分
    y_pred=clf.predict(X_test)
    print(type(y_pred))
    print(y_pred.shape)
    print('111')
    eval_accu=metrics.accuracy_score(y_test,y_pred) 
    print(eval_accu)
    eval_recall=metrics.recall_score(y_test,y_pred)
    eval_f1score=metrics.f1_score(y_test,y_pred)
    matrix=confusion_matrix(y_test,y_pred,labels=[0,1])
    print(matrix)
    eval_ac.append(eval_accu)
    eval_rc.append(eval_recall)
    eval_f1.append(eval_f1score)

    

    return clf

def test(clf,path1,feature_list,target):
    print(path1)
    data=np.loadtxt(path1,usecols=np.arange(1,130))
    print(data.shape)
    print("AAAA")
    X=data[:,feature_list]
    y=data[:,target]
    
    print(X.shape)
    print(y.shape)
    print(path1)
    start=time.time()
    y_pred=clf.predict(X)
    test_accu=metrics.accuracy_score(y,y_pred) 
    test_recall=metrics.recall_score(y,y_pred)
    test_f1s=metrics.f1_score(y,y_pred)
    test_ac.append(test_accu)
    test_rc.append(test_recall)
    test_f1.append(test_f1s)
    enduration=(time.time()-start)/y.size
    print(y.size)
    matrix=confusion_matrix(y,y_pred,labels=[0,1])
    print(matrix)
    fp=matrix[1,1]/(matrix[1,0]+matrix[1,1])
    false_1.append(fp)
    test_time.append(enduration)
    print(len(y))
    print(len(y_pred))
    
    ##get_failnode
    false_node.append(get_failnode(path1,y,y_pred))
    #test集上的其他得分
def get_failnode(path1,y,y_pred):
    
    f=open(path1,'r')
    r=f.readlines()
    count=0
    event={}
    dic2={}
    node=defaultdict(int)
    dic_node={}
    for item in r:
        keys=item.split(' ')
        temp=keys[0]
        count_s=temp.find('s')
        snap=temp[len('brokennode'):count_s]
        add=temp.find('+',count_s)
        end1=temp[count_s+1:add]
        end2=temp[add+2:]
        ##test:brokennode0+1s28+s39
        ##snap:0+1
        ##end1:28
        ##end2:39
        print(end1)
        print(end2)
        dic_node[end1]=1
        dic_node[end2]=1
        ##对事件初始化
        if snap not in dic2:
            node=defaultdict(int)
            dic2[snap]=1
            event[snap]=node
        ##初始化结束，每个事件前所有都标0
        event[snap][end1+'true']+=int(y[count])
        event[snap][end1+'pred']+=int(y_pred[count])
        event[snap][end1+'count']+=1
        event[snap][end1+'trueaverage']=event[snap][end1+'true']/event[snap][end1+'count']
        event[snap][end1+'predaverage']=event[snap][end1+'pred']/event[snap][end1+'count']
        event[snap][end2+'true']+=int(y[count])
        event[snap][end2+'pred']+=int(y_pred[count])
        event[snap][end2+'count']+=1
        event[snap][end2+'trueaverage']=event[snap][end2+'true']/event[snap][end2+'count']
        event[snap][end2+'predaverage']=event[snap][end2+'pred']/event[snap][end2+'count']
        ##计数器+1
        count+=1
        
        
    f.close()
    
    ##这里判断是否是fail node的阈值是0.7
    node=0
    true=[]
    pred=[]
    for ev1 in event:
        for en1 in dic_node:
            pred_node=0
            true_node=0
            judge=event[ev1][en1+'predaverage']
            if(ev1==en1):
                true_node=1
                print(judge)
            if(judge>=0.7):
                pred_node=1
            true.append(true_node)
            pred.append(pred_node)
    
    truearray=np.array(true)
    predarray=np.array(pred)
    accu=metrics.accuracy_score(truearray,predarray) 
    recall=metrics.recall_score(truearray,predarray)
    return recall


def get_feature(switch_count):
    
    ##假设为30维，[0,15)为一端,[15.30)为另一端
    feature=8
    ##这里的问题是总共的维度是512维。512维的含义是 4*128
    ##time_epoch的意思是有4个时间切片
    ##这里的含义是[0:2)是数据包数量.[2,4)是重发包数量，[0,32)是自己的信息，[32,64]是邻居的信息
    ##epoch是每个的起点
    epoch=8
    sample_epoch=int(48*switch_count)
    half=int(sample_epoch/2)
    ##这里epoch是4（个特征）*2(邻居信息)*8(个swithc_count)

    ##没有重发包的版本
    feature_list=[]
    for e in range(epoch):
        base1=e*sample_epoch
        base2=e*sample_epoch+half
        for s in range(0,switch_count):
            for f in [0,1,4,5,6,7,8,9,10,11]:
            #for f in [0,1,4,5]:
                query1=base1+s*12+f
                query2=base2+s*12+f
                #query3=query1+96
                #query4=query2+96
                feature_list.append(query1)
                feature_list.append(query2)
                #feature_list.append(query3)
                #feature_list.append(query4)
    
    """
    start1_list=[(8*i)for i in range(0,switch_count)]
    start2_list=[(64+8*i)for i in range(0,switch_count)]
    end1_list=[(8*i+feature)for i in range(0,switch_count)]
    end2_list=[(64+8*i+feature)for i in range(0,switch_count)]
    print(start1_list)
    print(start2_list)
    print(end1_list)
    print(end2_list)

    feature_list=[]
    for i in range(switch_count):
        for j in range(start1_list[i],end1_list[i]):
            feature_list.append(j)
        for j in range(start2_list[i],end2_list[i]):
            feature_list.append(j)
    print(feature_list)
    """
    return feature_list

if __name__ =="__main__":
    
    
    global x
    x=[]    
    
    #eval 汇报的数据
    global eval_ac
    eval_ac=[]
    global eval_rc
    eval_rc=[]
    global eval_f1
    eval_f1=[]
    
    #switch_count [1,6)
    
    for switch_count in range(1,9):
        ###输出路径格式见服务器上的README.md版本
        path='3967_link_176_8_'+str(switch_count)+'_b.txt'
        target=384*int(switch_count)
        x.append(switch_count)
        print(switch_count)
        feature_l=[]
        feature_l=get_feature(switch_count)

        print(feature_l)
        train(path,feature_l,target)



    #画图
    """
    for i in range(1,9):
        x.append(i)
    eval_ac=[25,33,35,37,40,40,40,40]
    eval_rc=[36,38,38,39,39,39,39,39]
    print(eval_ac)
    print(eval_rc)
    for j in range(8):
        eval_ac[j]/=40
        eval_rc[j]/=40
    """
    print(eval_ac)
    print(eval_rc)
    fig,ax = plt.subplots()
    plt.plot(x,eval_ac,'cx--',label='Accuracy')
    plt.plot(x,eval_rc,'mo:',label='Recall')
    plt.plot(x,eval_f1,'bp-',label='F1')
    plt.xticks(x)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(fontsize=20)
    plt.ylim(0.5,1)
    #plt.xlabel('monitor counts')
    #plt.ylabel('score')
    ax.set_xlabel('Monitor counts', fontsize=20)
    ax.set_ylabel('Evaluation metric', fontsize=20)
    plt.show()
    reload(plt)
    
    ###停掉
    sys.exit(0)
    
    
    
    
    
    feature_list=get_feature(6)
    target=128
    model=train(path,feature_list,target)
    #path1='train_200.txt'
    #model1=train(path1,feature_list,target)
    global test_ac
    test_ac=[]
    global test_rc
    test_rc=[]
    global test_f1
    test_f1=[]
    
    global false_1
    false_1=[]
    global test_time
    test_time=[]
    
    global false_node
    false_node=[]
    

    test_list=[]
    dataset_list=[]
    
    ##single node failure部分
    
    for i in range(5,9):
        test_list.append('2_AS1221_8_40_'+str(i)+'.txt')
        test_list.append('2_GEANT_8_40_'+str(i)+'.txt')
        test_list.append('2_chinaNet_8_40_'+str(i)+'.txt')
    
    
    
    
    ##mutlitple部分
    """
    for i in range(1,9):
        test_list.append("chinaNetM_8_40_"+str(i)+'.txt')
    """
        

    ##进行测试，这部分不能删除
    dataset_list=[(i+1) for i in range(len(test_list))]
    for i in test_list:
        test(model,i,feature_list,target)
    ###
    x=dataset_list
    print(test_ac)
    print(test_rc)
    print(test_f1)
    fig,ax = plt.subplots()
    plt.plot(x,test_ac,'cx--',label='Accuracy')
    plt.plot(x,test_rc,'mo:',label='Recall')
    plt.plot(x,test_f1,'bp-',label='Weighted-F1')
    plt.xticks(x)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(fontsize=20)
    plt.ylim(0.7,1.2)
    #plt.xlabel('monitor counts')
    #plt.ylabel('score')
    ax.set_xlabel('Time interval ID', fontsize=20)
    ax.set_ylabel('Evaluation metric', fontsize=20)
    plt.show()
    reload(plt)
    
    
    
    
    

    ##这里是实验品，不要看
    print(false_node)
    y1=[]
    y2=[]
    y3=[]
    y4=[]
    for i in range(4):
        y1.append(false_node[3*i])
        y2.append(false_node[3*i+1])
        y3.append(false_node[3*i+2])

    x=np.arange(len(y1))
    x+=1

    width=0.2
    fig,ax = plt.subplots()
    ax.bar(x,y1,width,color='b', hatch='//')
    ax.bar(x+width,y2,width,hatch='||', color='w', ec='g', ls='--', lw=0.5)
    ax.bar(x+2*width,y3,width,hatch='\\',color='yellow', ec='r', ls='--', lw=0.5)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    ax.set_xticks(x +width)
    ax.set_xticklabels(x)
    plt.ylim(0.7,1.3)
    ax.set_xlabel('Time interval ID', fontsize=20)
    ax.set_ylabel('Recall', fontsize=20)
    plt.legend(['AS1221','GEANT','chinaNet'],fontsize=19)
    plt.show()
    
    
    sys.exit(0)
    ##画图拆解部分  16个数据集
    reload(plt)
    
    
    ##画图拆解部分  16个数据集
    y1=[]
    y2=[]
    y3=[]
    y4=[]
    for i in range(3):
        y1.append(test_ac[3*i])
        y2.append(test_ac[3*i+1])
        y3.append(test_ac[3*i+2])

    x=np.arange(len(y1))
    x+=1
    width=0.2
    fig,ax = plt.subplots()
    ax.bar(x,y1,width,color='b', hatch='//')
    ax.bar(x+width,y2,width,hatch='||', color='w', ec='g', ls='--', lw=0.5)
    ax.bar(x+2*width,y3,width,hatch='\\',color='yellow', ec='r', ls='--', lw=0.5)
    
    ax.set_xticks(x +width)
    ax.set_xticklabels(x)
    plt.ylim(0.5,0.7)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(['AS1221','GEANT','chinaNet'],fontsize=19)
    ax.set_xlabel('Time interval ID', fontsize=20)
    ax.set_ylabel('Accuracy', fontsize=20)
    plt.show()

    reload(plt)
    """
    print(test_ac)
    plt.bar(dataset_list,test_ac,color='green')
    plt.xlabel('dataset ID')
    plt.ylim(0.5,1)
    plt.xticks(dataset_list)
    plt.ylabel('accuracy')
    plt.show()
    
    reload(plt)
    """
    reload(plt)
    y1=[]
    y2=[]
    y3=[]
    y4=[]
    for i in range(3):
        y1.append(test_rc[3*i])
        y2.append(test_rc[3*i+1])
        y3.append(test_rc[3*i+2])

    x=np.arange(len(y1))+1
    width=0.2
    fig,ax = plt.subplots()
    ax.bar(x,y1,width,color='b', hatch='//')
    ax.bar(x+width,y2,width,hatch='||', color='w', ec='g', ls='--', lw=0.5)
    ax.bar(x+2*width,y3,width,hatch='\\',color='yellow', ec='r', ls='--', lw=0.5)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    ax.set_xticks(x +width)
    ax.set_xticklabels(x)
    plt.ylim(0.7,1.3)
    ax.set_xlabel('Time interval ID', fontsize=20)
    ax.set_ylabel('Recall', fontsize=20)
    plt.legend(['AS1221','GEANT','chinaNet'],fontsize=19)
    plt.show()
    """
    plt.bar(dataset_list,test_rc,color='green')
    plt.xlabel('dataset ID')
    plt.ylim(0.5,1)
    plt.xticks(dataset_list)
    plt.ylabel('recall')
    plt.show()
    """



    reload(plt)
    y1=[]
    y2=[]
    y3=[]
    y4=[]
    for i in range(3):
        y1.append(false_1[3*i])
        y2.append(false_1[3*i+1])
        y3.append(false_1[3*i+2])

    x=np.arange(len(y1))+1
    width=0.2
    fig,ax = plt.subplots()
    ax.bar(x,y1,width,color='b', hatch='//')
    ax.bar(x+width,y2,width,hatch='||', color='w', ec='g', ls='--', lw=0.5)
    ax.bar(x+2*width,y3,width,hatch='\\',color='yellow', ec='r', ls='--', lw=0.5)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    ax.set_xticks(x +width)
    ax.set_xticklabels(x)
    plt.ylim(0.7,1.3)
    ax.set_xlabel('Time interval ID', fontsize=20)
    ax.set_ylabel('Accuracy of brokenlink', fontsize=20)
    plt.legend(['AS1221','GEANT','chinaNet'],fontsize=19)
    plt.show()