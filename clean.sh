sudo mn -c
sudo ps -ef|grep chinaNet.py |grep -v grep|awk '{print $2}'|sudo xargs kill -9
sudo ps -ef|grep traffic.py |grep -v grep|awk '{print $2}'|sudo xargs kill -9
sudo ps -ef|grep defunct |grep -v grep|awk '{print $2}'|sudo xargs kill -9
sudo ps -ef|grep tcpdump |grep -v grep|awk '{print $2}' |sudo xargs kill -9
sudo ps -ef|grep start.sh |grep -v grep|awk '{print $2}' |sudo xargs kill -9
