import math


def get_src_dst_info(path):
    # 功能：从当前path下的throughput.txt中获取TCP流的信息
    # 输入：path：报文所在的路径，一般为./brokennodei
    # 输出：src_dst_info：字典，src_dst_info[src]=[dst1,dst2,...]，代表存在从h_src到h_dst1,h_dst2,...的TCP流
    src_dst_info = {}
    f_throughput = open(path + 'throughput.txt', 'r')
    lines = f_throughput.readlines()
    for line_now in lines:
        keys = line_now.split()
        src = keys[0][1:]  # h_src
        dst = keys[1][1:]  # h_dst

        if src not in src_dst_info:
            src_dst_info[src] = []
        src_dst_info[src].append(dst)

    return src_dst_info


def get_parameters(path, min_burst_length):
    # 功能：根据报文记录，得到ON/OFF间隔服从指数分布与Pareto分布时的相应参数的估计值，并写入文件parameters.txt中
    # 输入：path：报文所在的路径，一般为./brokennodei
    #      min_burst_length：突发序列的最小时长tau，该方法将在tau的时间尺度上考察流量的自相关性及突发性
    # 输出：parameters：parameters[src][dst]=[lambda_on,lambda_off,gamma_on,gamma_off]，存有假设ON/OFF间隔各自服从指数分布
    #          exp(lambda)与Pareto分布Pareto(tau,gamma)时的参数估计值
    src_dst_info = get_src_dst_info(path)

    # parameters.txt的各列为：流起点src，流终点dst，ON间隔的指数分布exp(lambda)参数估计值，OFF间隔的指数分布exp(lambda)参数估计值，
    #     ON间隔的Pareto分布Pareto(tau,gamma)参数估计值，OFF间隔的Pareto分布Pareto(tau,gamma)参数估计值
    f_paras = open('parameters.txt', 'w')
    f_paras.write('src\tdst\texp_lambda_on\texp_lambda_off\tpareto_gamma_on\tpareto_gamma_off\texp_lambda_on_off\n')
    f_paras.write('min_burst_length=' + str(min_burst_length) + 's\n')

    parameters = {}
    for i in range(nodes_count):
        if str(i) not in src_dst_info:
            continue
        parameters[str(i)] = {}

        # 从si.csv中寻找以hi为源的TCP流，并考察其表现
        f_src_now = open(path + 's' + str(i) + '.csv', 'r')
        lines = f_src_now.readlines()

        burst_start_time = {}  # burst_start_time[dst]=[a0,a1,...]，ak表示流(hi,h_dst)的第k个突发序列的到达时刻
        burst_end_time = {}  # burst_end_time[dst]=[w0,w1,..]，wk表示流(hi,h_dst)的第k个突发序列的离开时刻
        time_before = {}
        for dst in src_dst_info[str(i)]:
            parameters[str(i)][dst] = []
            burst_start_time[dst] = []
            burst_end_time[dst] = []
            time_before[dst] = float('-inf')  # time_before[dst]用于记录流(hi,h_dst)的当前突发序列延续到了何时

        for line_now in lines:
            # 过滤掉无关的报文记录
            if 'TCP' not in line_now:
                continue
            keys = line_now.split()
            src = str(int(keys[2].split('.')[-1]) - 1)
            if src is not str(i):
                continue
            dst = str(int(keys[4].split('.')[-1]) - 1)
            if dst not in src_dst_info[src]:
                continue

            time_now = float(keys[1])
            # case：若当前报文和当前突发序列的间隔大于tau，则说明此时已是下一个突发序列；否则当前报文仍属于当前突发序列
            if time_now - time_before[dst] > min_burst_length:
                if time_before[dst] > float('-inf'):
                    burst_end_time[dst].append(time_before[dst])  # 标记当前突发序列的结束时刻
                burst_start_time[dst].append(time_now)  # 并标记新的突发序列的到达时刻
            time_before[dst] = time_now  # 更新流(hi,h_dst)的当前突发序列的延续时刻

        # 求出ON/OFF间隔的参数估计量
        for dst in src_dst_info[src]:
            sum_on = 0.0
            sum_off = 0.0
            product_on = 1.0
            product_off = 1.0
            n = len(burst_start_time[dst]) - 1
            for k in range(n):
                sum_on += (burst_end_time[dst][k] - burst_start_time[dst][k]) / min_burst_length
                sum_off += (burst_start_time[dst][k + 1] - burst_end_time[dst][k]) / min_burst_length
                product_on *= (burst_end_time[dst][k] - burst_start_time[dst][k]) / min_burst_length
                product_off *= (burst_start_time[dst][k + 1] - burst_end_time[dst][k]) / min_burst_length
            sum_on_off = sum_on + sum_off

            # 假定间隔服从指数分布exp(lambda)时，lambda的最大似然估计量为n/sum{xi}
            exp_lambda_on = n / sum_on
            exp_lambda_off = n / sum_off
            # 假定间隔服从Pareto分布Pareto(tau,gamma)时，gamma的最大似然估计量为n/sum{ln(xi)}
            pareto_gamma_on = n / math.log(product_on)
            pareto_gamma_off = n / math.log(product_off)
            # 假定突发序列到达间隔服从指数分布exp(lambda)时，lambda的最大似然估计量为n/sum{xi}
            exp_lambda_on_off = n / sum_on_off

            # 将结果写入文件并保存
            f_paras.write(src + '\t' + dst + '\t' + '%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n'
                          % (exp_lambda_on, exp_lambda_off, pareto_gamma_on, pareto_gamma_off, exp_lambda_on_off) )
            parameters[src][dst].append(exp_lambda_on)
            parameters[src][dst].append(exp_lambda_off)
            parameters[src][dst].append(pareto_gamma_on)
            parameters[src][dst].append(pareto_gamma_off)
            parameters[src][dst].append(exp_lambda_on_off)

    f_paras.close()
    return parameters


global nodes_count
nodes_count = 42

if __name__ == '__main__':
    for i in range(nodes_count):
        brokennode_path = 'brokennode' + str(i) + '/'
        get_parameters(brokennode_path, 0.05)
