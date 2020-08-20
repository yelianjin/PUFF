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
参考 DevFlow Freeway 