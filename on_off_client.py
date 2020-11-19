# -*- coding:UTF-8 -*-
import socket
import time
import sys
import random
def decompose_and_shuffle(time_string):
    # 功能：将输入的时间组成的字符串还原并随机打乱成一个时间列表
    # 输入：time_string：字符串类型，形如’t1+t2+...+tn‘，其中ti是一个四位有效数字的时间
    # 输出：time_list：由time_string还原而来的浮点数列表，其中存储的时间的顺序相比time_string是打乱过的
    str_list = time_string.split('+')

    time_list = []
    for time_str in str_list:
        time_list.append(float(time_str))
    #random.shuffle(time_list)

    return time_list


def send_data(time_length):
    # 功能：让该client以恒定速率（bw_bps）向server发送数据，时长为time_length秒
    # 输入：time_length：本次发送数据的时长，单位为秒
    global totalBytes

    data_size = int(time_length * bw_bps / 8)  # 计算按照bw_bps的带宽，本次发送应发送多少Byte的数据
    if data_size > size - totalBytes:
        data_size = size - totalBytes
    totalBytes += data_size  # 更新已发送的字节数
    print('Sending Data: ' + str(data_size) + ' Bytes.')

    while data_size > 1448:
        so.send(P1.encode())
        data_size -= 1448
    so.send(P1[:data_size].encode())
    print('Sending Accomplished.')


def on_off_scheduler(on_times, off_times, count):
    # 功能：让client按照on_times以及off_times列表的元素来进行ON/OFF状态交替
    # 输入：on_times：浮点数列表，其元素表示在ON状态中停留的时长。当处于ON状态时，client会以恒定速率发送数据
    #      off_times：浮点数列表，其元素表示在OFF状态中停留的时长。当处于OFF状态时，client会停止发送数据
    #      count：client进行ON/OFF状态交替的次数 
    global totalBytes

    pos_now = 0  # pos_now标记当前是第几次ON/OFF状态交替
    while 1:
        if pos_now >= count and size>=totalBytes:  # case：发送（即将）结束
            print('Scheduler: Run out of times.')
            return
        if pos_now >=count and size>=totalBytes:
            pos_now=0

        if size <= totalBytes:
            print('Scheduler: All of data has been sent.')
            return

        print('Scheduler: Client ON for ' + str(on_times[pos_now]) + ' sec.')
        send_data(on_times[pos_now])
        print('Scheduler: Client OFF for ' + str(off_times[pos_now]) + ' sec.')
        time.sleep(off_times[pos_now])
        pos_now += 1

if __name__ == "__main__":
    global so
    ip_source=sys.argv[1]
    ip_dst=sys.argv[2]
    global size
    size=int(sys.argv[3])
    global totalBytes

    ttotalBytes=0
    port_dst=10000+int(sys.argv[6])
    
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr=(ip_dst,port_dst)
    so.connect(addr)
    print('connected')
    global P1
    P1=''
    for i in range(1448):
        P1+='b'


    global totalBytes  # 目前已经发送的数据载荷量，单位为Byte
    totalBytes = 0

    # 将传入的存有ON/OFF时间的字符串还原为浮点数列表，并随机打乱
    temp_on = sys.argv[4]
    temp_off = sys.argv[5]
    on_times = decompose_and_shuffle(temp_on)
    off_times = decompose_and_shuffle(temp_off)


    global bw_bps
    bw_bps=100*1024*1024
    

    on_off_scheduler(on_times, off_times, len(on_times))

    so.send('quit'.encode())
    so.close()

    print('Sending: ' + str(totalBytes) + ' of ' + str(size) + ' Bytes.')
