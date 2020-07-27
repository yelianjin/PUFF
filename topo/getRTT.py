def add2dimDict(theDict, key_a, key_b, val):
    # 功能：将索引对{key_a:{key_b:val}}添加到字典theDict中
    # 备注：因为解释器不能确定第一维的索引是否已经存在于字典theDict中，所以对二维字典直接赋值会报错（类似二维数组），需如下做才能成功添加索引对

    if key_a in theDict:
        theDict[key_a].update({key_b: val})
    else:
        theDict.update({key_a: {key_b: val}})


def get_topo(filename):
    # 功能：通过读取设置网络拓扑的.py文件，来获取拓扑中的交换机信息以及链路信息
    # 要求：filename：目标文件的路径名
    #      目标文件中必须先连续逐行地出现添加交换机的语句，在若干行语句之后再连续逐行地出现添加链路（且显式注明时延参数'delay=tms'）的语句
    # 输出：switch2num：存储所有{交换机名称:交换机编号}的索引对（例如{'Lhasa':'s0'}），即保存网络中的交换机结点信息
    #      edge_cost：存储所有{交换机s1:{交换机s2:链路<s1,s2>时延}}的索引对，即保存网络中的链路信息

    f = open(filename)  # 读取设置网络拓扑的.py文件
    r = f.readlines()

    line_now = 0  # line_now表示当前所在行数
    switch2num = {}
    edge_cost = {}

    # 定位到添加交换机结点的代码部分
    while 1:
        if line_now >= len(r):
            break
        if r[line_now].find('addSwitch') != -1:
            break
        line_now += 1

    # 将交换机结点的信息添加到字典switch2num中
    while 1:
        if line_now >= len(r):
            break
        if r[line_now].find('addSwitch') == -1:
            break
        temp_str = r[line_now].split('=')[0].strip()  # 提取交换机名称
        switch_num = r[line_now].split('\'')[1]  # 提取交换机编号
        switch2num[temp_str] = switch_num  # 添加相应索引对
        line_now += 1
    # print(switch2num)

    # 定位到添加链路的代码部分（必须显式注明时延参数'delay=tms'）
    while 1:
        if line_now >= len(r):
            break
        if (r[line_now].find('addLink') != -1) and (r[line_now].find('delay') != -1):
            break
        line_now += 1

    # 将链路的信息（起点，终点，时延）添加到字典edge_cost中
    while 1:
        if line_now >= len(r):
            break
        if (r[line_now].find('addLink') == -1) or (r[line_now].find('delay') == -1):
            break
        temp_str = r[line_now][r[line_now].find('(') + 1:r[line_now].find('ms\'')]  # 提取addLink方法的参数段部分
        delay = float(temp_str.split('delay=\'')[-1])  # 提取链路时延
        temp_list = temp_str.split(',')
        switch1 = temp_list[0].strip()  # 提取链路起点
        switch2 = temp_list[1].strip()  # 提取链路终点
        add2dimDict(edge_cost, switch2num[switch1], switch2num[switch2], delay)  # 添加链路信息（默认该网络为无向图）
        add2dimDict(edge_cost, switch2num[switch2], switch2num[switch1], delay)
        line_now += 1
    # print(edge_cost)

    return switch2num, edge_cost


def get_realRTT(short_all, edge_cost):
    # 功能：计算各交换机结点之间（按最短路径传输数据时）的实际RTT，并同时计算该RTT集合的最大值、最小值、中位数及算术平均数
    # 要求：交换机名称与交换机编号的对应关系
    #      short_all：各交换机结点之间（按跳数计）的最短路径，其中保存的索引对为{起点s1:{终点s2:路径[s1,...,s2]}}
    #      edge_cost：网络中的链路时延信息，其中保存的索引对为{交换机s1:{交换机s2:链路<s1,s2>的时延}}
    # 输出：rtt_all：存储所有{起点s1:{终点s2:s1到s2的RTT}}的索引对，即保存各交换机结点之间（按最短路径传输数据时）的RTT
    #      rtt_min：rtt_all的最小值
    #      rtt_max：rtt_all的最大值
    #      rtt_midMean：rtt_all的中位数
    #      rtt_arithMean：rtt_all的算术平均数

    rtt_all = {}
    temp = []

    # 计算结点i到结点j之间（按最短路径传输数据时）的RTT，并存储于rtt_all中
    for i in range(len(short_all)):
        for j in range(len(short_all)):
            if i == j:
                add2dimDict(rtt_all, 's' + str(i), 's' + str(j), 0.0)
                continue
            temp_cost = 0.0
            list_ptr = short_all['s' + str(i)]['s' + str(j)]
            for k in range(len(list_ptr) - 1):
                temp_cost += edge_cost[list_ptr[k]][list_ptr[k + 1]]
            add2dimDict(rtt_all, 's' + str(i), 's' + str(j), 2 * temp_cost)
            sum += 2 * temp_cost
            temp.append(2 * temp_cost)

    # temp为一个存储了所有结点对RTT值的列表，通过temp的辅助便可容易地计算RTT集合的最大值、最小值、中位数以及算术平均数
    temp.sort()
    l = len(temp)
    rtt_min = temp[0]
    rtt_max = temp[l - 1]
    rtt_midMean = temp[l // 2]
    rtt_arithMean = sum / l

    return rtt_all, rtt_max, rtt_min, rtt_midMean, rtt_arithMean
