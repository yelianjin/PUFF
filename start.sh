#########################################################################
# File Name: start.sh
# Author: test
for i in `seq 36 36`
do
	python chinaNet.py $i
	sudo ps -ef|grep chinaNet.py |grep -v grep |awk '{print $2}'|sudo xargs kill -9
	sudo ps -ef|grep traffic.py |grep -v grep |awk '{print $2}'|sudo xargs kill -9
	sudo ps -ef|grep defunct |grep -v grep |awk '{print $2}'|sudo xargs kill -9
	sudo ps -ef|grep tcpdump |grep -v grep |awk '{print $2}'|sudo xargs kill -9
	for j in `seq 0 42`
	do 
		mergecap -w s$j.pcap s$j-eth*.pcap
		tshark -r s$j.pcap >s$j.csv
		#python feature1.py
	done
	mkdir brokennode$i
	mv *.csv *.txt tcplook.sh brokennode$i
	rm -rf *.pcap
done
cp brokennode0/neighbors.txt neighbors.txt
#python feature2.py
#python feature3.py
