#########################################################################
# File Name: start.sh
# Author: test
for k in `seq 0 0`
do
	for i in `seq 0 0`
	do
		python chinaNet.py $i
		echo "I am a killer"
		sudo ps -ef|grep chinaNet.py |grep -v grep |awk '{print $2}'|sudo xargs kill -9
		sudo ps -ef|grep traffic.py |grep -v grep |awk '{print $2}'|sudo xargs kill -9
		sudo ps -ef|grep defunct |grep -v grep |awk '{print $2}'|sudo xargs kill -9
		sudo ps -ef|grep tcpdump |grep -v grep |awk '{print $2}'|sudo xargs kill -9
		sudo ps -ef|grep client.py |grep -v grep |awk '{print $2}'|sudo xargs kill -9
		sudo ps -ef|grep server.py |grep -v grep |awk '{print $2}'|sudo xargs kill -9
	
		for j in `seq 0 41`
		do 
			mergecap -w s$j.pcap s$j-eth*.pcap
			tshark -r s$j.pcap >s$j.csv
			#python feature1.py
		done
		mkdir brokennode$i
		mv *.csv *.txt tcplook.sh brokennode$i
		cp brokennode0/neighbors.txt neighbors.txt
		mkdir pcap_data
		mv *.pcap pcap_data
		mv pcap_data brokennode$i
	done
	mkdir data$k
	mv brokennode* data$k
	#python feature2.py
done
