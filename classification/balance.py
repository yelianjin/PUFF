import sys
import random
"""
f=open('train.txt','r')
f_balance=open('train2.txt','a')
count=0
count_t=0
count_0=191
r=f.readlines()
len_f=len(r)
for i in range(count_0):
    j=random.randint(0,len_f)
    item=r[j]
    keys=item.split(' ')
    target=keys[30].strip()
    while(target!='0'):
        j=random.randint(0,len_f)
        item=r[j]
        keys=item.split(' ')
        target=keys[30].strip()
    f_balance.write(item)
f_balance.close()
f.close()
"""
if __name__=='__main__':
    f=open('Tinet_link_200.txt','r')
    f_balance=open('Tinet_link_200_b.txt','w')
    r=f.readlines()
    len_f=len(r)
    count=0
    global a
    a=1537
    for item in r:
        keys=item.split(' ')
        print(len(keys))
        if(len(keys)==514):
            continue
        try:
            target=keys[a].strip()
        except:
            continue
        print(target)
        if (target=='1'):
            f_balance.write(item)
            count+=1

    print(count)
    len_r1=count
    count2=0
    for i in range(len_r1):
        j=random.randint(0,len_f)
        item=r[j]
        keys=item.split(' ')
        try:
            target=keys[a].strip()
        except:
            continue
        while(target!='0'):
            j=random.randint(0,len_f)
            item=r[j]
            keys=item.split(' ')
            try:
                target=keys[a].strip()
            except:
                continue
        f_balance.write(item)
        count2+=1
    f.close()
    f_balance.close()
    print(count2)