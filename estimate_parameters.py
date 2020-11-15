import math


def get_src_dst_info(path):
    # 功能：从当前path下的throughput.txt中获取TCP流的信息
    # 输入：path：报文所在的路径，一般为./brokennodei
    # 输出：src_dst_info：字典，src_dst_info[src][dst]=[size]，代表存在从h_src到h_dst的TCP流，其数据量为size
    src_dst_info = {}
    f_throughput = open(path + 'throughput.txt', 'r')
    lines = f_throughput.readlines()
    for line_now in lines:
        keys = line_now.split()
        src = keys[0][1:]  # h_src
        dst = keys[1][1:]  # h_dst
        size = keys[-1]  # size

        if src not in src_dst_info:
            src_dst_info[src] = {}
        src_dst_info[src][dst] = size
    return src_dst_info


def interval_number(time, interval_length):
    # 功能：将时间轴按照长度interval_length编号，并返回时刻time所对应的时间间隔的序号
    # 输入：time：时刻
    #      interval_length：时间间隔长度
    # 输出：serial_number：时刻time所对应的时间间隔序号
    serial_number = math.ceil(time / interval_length)
    return serial_number


def get_parameters(path, min_burst_length):
    # 功能：根据报文记录，得到ON/OFF间隔服从指数分布与Pareto分布时的相应参数的估计值，并写入文件parameters.txt中
    # 输入：path：报文所在的路径，一般为./brokennodei
    #      min_burst_length：突发序列的最小时长tau，该方法将在tau的时间尺度上考察流量的自相关性及突发性
    # 输出：parameters：parameters[src][dst]=[lambda_on,lambda_off,gamma_on,gamma_off,lambdaon_off]，存有假设ON/OFF间隔各自服
    #          从指数分布exp(lambda)与Pareto分布Pareto(tau,gamma)时的参数估计值，以及突发序列间隔服从指数分布时的参数估计值
    src_dst_info = get_src_dst_info(path)

    # parameters.txt的各列为：流起点src，流终点dst，ON间隔的指数分布exp(lambda)参数估计值，OFF间隔的指数分布exp(lambda)参数估计值，
    #     ON间隔的Pareto分布Pareto(tau,gamma)参数估计值，OFF间隔的Pareto分布Pareto(tau,gamma)参数估计值
    f_paras = open(path + 'parameters.txt', 'w')
    f_paras.write('src\tdst\tflow_size\tburst\t'
                  'exp_lambda_on\texp_lambda_off\tpareto_gamma_on\tpareto_gamma_off\texp_lambda_on_off\n')
    f_paras.write('min_burst_length=' + str(min_burst_length) + 's\n')

    parameters = {}
    for i in range(nodes_count):
        if str(i) not in src_dst_info:
            continue
        parameters[str(i)] = {}

        # 从si.csv中寻找以hi为源的TCP流，并考察其表现
        f_src_now = open(path + 's' + str(i) + '.csv', 'r', encoding='utf-8')
        lines = f_src_now.readlines()
        print('Processing ' + path + 's' + str(i) + '.csv now.')

        burst_start_time = {}  # burst_start_time[dst]=[a0,a1,...]，ak表示流(hi,h_dst)的第k个突发序列的到达时刻
        burst_end_time = {}  # burst_end_time[dst]=[w0,w1,..]，wk表示流(hi,h_dst)的第k个突发序列的离开时刻
        time_before = {}
        for dst in src_dst_info[str(i)]:
            parameters[str(i)][dst] = []
            burst_start_time[dst] = []
            burst_end_time[dst] = []
            time_before[dst] = -1  # time_before[dst]用于记录流(hi,h_dst)的当前突发序列延续到了何时

        for line_now in lines:
            # 过滤掉无关的报文记录
            if 'TCP' not in line_now:
                continue
            keys = line_now.split()
            src = str(int(keys[2].split('.')[-1]) - 1)
            if src != str(i):
                continue
            dst = str(int(keys[4].split('.')[-1]) - 1)
            if dst not in src_dst_info[src]:
                continue

            time_now = interval_number(float(keys[1]), min_burst_length)
            # case：若当前报文和当前突发序列的间隔大于tau，则说明此时已是下一个突发序列；否则当前报文仍属于当前突发序列
            if time_now - time_before[dst] > 1:
                if time_before[dst] > 0:
                    burst_end_time[dst].append(time_before[dst])  # 标记当前突发序列的结束时刻
                burst_start_time[dst].append(time_now)  # 并标记新的突发序列的到达时刻
            time_before[dst] = time_now  # 更新流(hi,h_dst)的当前突发序列的延续时刻

        print(burst_start_time)
        print(burst_end_time)

        # 求出ON/OFF间隔的参数估计量
        for dst in src_dst_info[str(i)]:
            sum_on = 0.0
            sum_off = 0.0
            sum_log_on = 0.0
            sum_log_off = 0.0
            n = len(burst_start_time[dst]) - 1
            if n <= 1:
                continue
            for k in range(n):
                sum_on += burst_end_time[dst][k] - burst_start_time[dst][k] + 1
                sum_off += burst_start_time[dst][k + 1] - burst_end_time[dst][k] - 1
                sum_log_on += math.log(burst_end_time[dst][k] - burst_start_time[dst][k] + 2)
                sum_log_off += math.log(burst_start_time[dst][k + 1] - burst_end_time[dst][k])
            sum_on_off = sum_on + sum_off

            # 假定间隔服从指数分布exp(lambda)时，lambda的最大似然估计量为n/sum{xi}
            exp_lambda_on = n / sum_on
            exp_lambda_off = n / sum_off
            # 假定间隔服从Pareto分布Pareto(1,gamma)时，gamma的Bayes估计量为sqrt[n(n+1)]/sum{ln(1+xi)}
            pareto_gamma_on = math.sqrt(n * n + n) / sum_log_on
            pareto_gamma_off = math.sqrt(n * n + n) / sum_log_off
            # 假定突发序列到达间隔服从指数分布exp(lambda)时，lambda的最大似然估计量为n/sum{xi}
            exp_lambda_on_off = n / sum_on_off

            # 将结果写入文件并保存
            size = src_dst_info[str(i)][dst]
            f_paras.write(str(i) + '\t' + dst + '\t' + size + '\t' + str(n+1) + '\t'
                          + '%.12f\t%.12f\t%.12f\t%.12f\t%.12f\n'
                          % (exp_lambda_on, exp_lambda_off, pareto_gamma_on, pareto_gamma_off, exp_lambda_on_off))
            parameters[str(i)][dst].append(exp_lambda_on)
            parameters[str(i)][dst].append(exp_lambda_off)
            parameters[str(i)][dst].append(pareto_gamma_on)
            parameters[str(i)][dst].append(pareto_gamma_off)
            parameters[str(i)][dst].append(exp_lambda_on_off)

    f_paras.close()
    return parameters


global nodes_count
nodes_count = 42

if __name__ == '__main__':
    min_burst_time = 0.01
    for i in range(nodes_count):
        brokennode_path = 'brokennode' + str(i) + '/'
        get_parameters(brokennode_path, min_burst_time)
