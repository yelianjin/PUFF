# PUFF  
start.sh  启动入口  传入参数 brokennode  
chinaNet.py  建立chinaNet拓扑，调用traffic.py产生流量，打开抓包  
mergecap/tshark 解析生成的pcap格式  
feature1.py  1.时间对齐 2.时间切片  
feature2.py  对每一份时间片进行特征化  
feature3.py  选点，产生data.txt  
data.sh       

# 打流的设置  
80%小流（0-1M）  
20%大流(1-10M)  
考虑一个泊松分布  
根据分布函数进行参数的修正 
令F(x<=1M)=0.8,xmin=1500 
得相应的函数a=0.24 
开始参考代码进行设计 
参考 DevFlow Freeway 

# Bug点  
chinaNet2_data/data0/brokennode38/{0-37}.csv  

