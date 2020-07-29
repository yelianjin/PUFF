# PUFF-topo  
PUFF的拓扑性质-汇报端到端的RTT时延  
GEANT:  最大值:100.614±5ms  最小值:0.558ms  中位数:23.867±1ms  算术平均数:26.718±2ms  25%分位数:14.752±0.4ms  75%分位数:35.290±2ms

chinaNet:  最大值:73.465±1ms  最小值:0.818ms  中位数:23.345±0.4ms  算术平均数:25.380±0.4ms  25%分位数:15.507±0.2ms  75%分位数:33.912±1ms

AS1221:  最大值:108ms  最小值:2ms  中位数:28ms  算术平均数:31.859±0.1ms  25%分位数:18ms  75%分位数:44ms

注：RTT是采用两倍端到端时延的方式来计算的。另外由于计算最短路径使用的是基于跳数的BFS，得到的最短路径有一定随机性，所以得到的RTT统计量会有小范围的变化  

#assessing-mininet  
拓扑地址 http://www.topology-zoo.org/dataset.html
上的所有.graphml文件
爬虫爬下来/手动下下来所有的graphml文件    
其实不需要neighbors.txt，本身生成的*.py中就有邻居关系  
通过assessing-mininet/parser，参考文件中的README.md进行操作，再通过get_RTT.py进行双向RTT的计算。  
汇报几个中位数/算术平均数明显异于chinaNet/GEANT/AS1221的拓扑  