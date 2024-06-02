import hashlib
import os
import sys
from random import choice, sample
import concurrent.futures
import time
import threading
import random
import pyfiglet
if not os.path.exists('.\log'):
    os.makedirs('.\log')
import hashlib
nodeplan = 'node'
networkplan = 'lstm'

# if len(sys.argv) > 1:
#     nodeplan = sys.argv[1]
# if len(sys.argv) > 2:
#     networkplan = sys.argv[2]

# Node = __import__(nodeplan).Node
# Network = __import__(networkplan).Network

from Network import Network
from lstm import Node
# 根据需要添加更多的导入选项

def time_elapsed(start_time, mess):
    # print(f'\n---{mess} in: {(time.time() - start_time)} seconds ---')
    pass

def measure_performance(chord_net, node_ids, num_trials=50):
    results_insert = []
    results_search = []

    for num_nodes in [10, 50, 100, 200, 500, 1000, 2000, 10000]:  # 不同的节点数
    # for num_nodes in [10]:
        print(f'\nTesting with {num_nodes} nodes...')
        results_insert = []  # 重置插入结果列表
        results_search = []  # 重置查找结果列表

        # 创建网络
        node_ids = sample(range(Node.ring_size), num_nodes)
        chord_net = Network(Node.m, node_ids)
        for node_id in node_ids:
            chord_net.insert_node(node_id)

        inserted_data = []  # 存储插入的数据

        # 插入操作
        for _ in range(num_trials):
            data = str(choice(range(10000)))  # 随机数据
            start_time = time.time()
            hops_insert = chord_net.insert_data(data)
            time_elapsed(start_time, 'insert data')
            results_insert.append(hops_insert)  # 保留每次插入操作的结果
            inserted_data.append(data)  # 记录插入的数据


        # 查找操作
        for data in inserted_data:
            num_searches = choice(range(5, 10))  # 随机查找次数（4-10次）
            for _ in range(num_searches):
                start_time = time.time()
                hops_search = chord_net.find_data(data)
                time_elapsed(start_time, 'search data')
                results_search.append(hops_search)  # 保留每次查找操作的结果

        # 计算平均值
        average_hops_insert = sum(results_insert) / len(results_insert)
        average_hops_search = sum(results_search) / len(results_search)

        # 将平均值和次数附加在日志文件末尾
        with open(f".\lognew\logNode{nodeplan}Network{networkplan}.txt", 'a') as file:
            file.write(f"Number of Nodes: {num_nodes}\n")
            file.write(f"Average Hops (Insert): {average_hops_insert}\n")
            file.write(f"Average Hops (Search): {average_hops_search}\n")
            file.write(f"Number of Trials: {num_trials}\n\n")


def create_network():
    sys.setrecursionlimit(10000000)

    ascii_banner = pyfiglet.figlet_format('CHORD')
    print(ascii_banner)
    print('Developed by: Konstantinos Bourantas[23 6145]')
    print('---------------------------------------------')

    Node.m = 22
    m_par = 22
    Node.ring_size = 2 ** m_par

    print(f'Creating network with total capacity {Node.ring_size} nodes.')
    num_nodes = 1

    while(num_nodes > 2**m_par):
        print('[-]Numbers of nodes cant be bigger than ring size.')
        num_nodes = int(input('Enter number of nodes : '))

    num_data = 30

    print('--------------------------------------------')

    node_ids = sample(range(Node.ring_size), num_nodes)

    chord_net = Network(m_par, node_ids)

    start_time = time.time()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        created_nodes = executor.map(
            chord_net.create_node, node_ids, chunksize=100)
        for node in created_nodes:
            chord_net.nodes.append(node)

    # split nodes insertion into the two threads
    half = len(chord_net.nodes)//2

    t1 = threading.Thread(target=chord_net.insert_nodes,
                          args=(chord_net.nodes[:half],))
    t2 = threading.Thread(target=chord_net.insert_nodes,
                          args=(chord_net.nodes[half:],))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
    time_elapsed(start_time, 'Network created')

    # insert many fake data to network
    if(num_data > 0):
        chord_net.generate_fake_data(num_data)

    # 测量性能
    measure_performance(chord_net, node_ids)

if __name__ == '__main__':

    create_network()
