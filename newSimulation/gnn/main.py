import hashlib
import os
import sys
from random import choice, sample
import concurrent.futures
import time
import threading
import pydotplus
from PIL import Image
import pyfiglet
import torch
import torch_geometric

from Node import Node
from Network import Network
from GNN import GNNModel  # Import the GNN model

plan = "gnn"


################################################################################################################
def measure_performance(chord_net, node_ids, num_trials=2000):
    results = []

    for num_nodes in [10, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 100000, 500000]:  # 不同的节点数
        print(f'\nTesting with {num_nodes} nodes...')
        results = []  # 重置results列表

        # 创建网络
        node_ids = sample(range(Node.ring_size), num_nodes) 
        chord_net = Network(Node.m, node_ids)
        for node_id in node_ids:
            chord_net.insert_node(node_id)

        # 插入操作
        for _ in range(num_trials):
            data = str(choice(range(10000)))  # 随机数据
            start_time = time.time()
            hops_insert = chord_net.insert_data(data)
            time_elapsed(start_time, 'insert data')
            results.append(hops_insert)  # 保留每次插入操作的结果

        # 计算平均值
        average_hops = sum(results) / len(results)

        # 将平均值和次数附加在日志文件末尾
        with open(f"log{plan}.txt", 'a') as file:
            file.write(f"Number of Nodes: {num_nodes}\n")
            file.write(f"Average Hops: {average_hops}\n")
            file.write(f"Number of Trials: {num_trials}\n\n")

        # 输出到CSV文件，文件名包含num_nodes
        # filename = f'performance_results_plan{plan}_{num_nodes}_nodes.csv'
        
        # with open(f"./run/plan{plan}/" + filename, 'a', newline='') as file:  # 使用'a'模式附加到文件末尾
        #     writer = csv.writer(file)
        #     writer.writerow(['Number of Nodes', 'Operation', 'Hops', 'Average Hops']) 
        #     writer.writerows([[num_nodes, 'insert', result, average_hops] for result in results])

def time_elapsed(start_time, mess):
    print(f'\n---{mess} in: {(time.time() - start_time)} seconds ---')


def show_menu(chord_net, node_ids):

    while True:
        chord_net.periodic_fix()
        print('================================================')
        print('1.Insert new node to network')
        print('2.Find data in the network')
        print('3.Insert data to network')
        print('4.Print network graph')
        print('5.Print network info')
        print('6.Delete node from network')
        print('7.Exit')
        print('================================================')

        choice = input('Select an operation: ')

        print('\n')

        if(choice == '1'):
            # insert a single node to network
            node_id = int(input('[->]Enter node id: '))
            if node_id not in node_ids:
                start_time = time.time()

                chord_net.insert_node(node_id)
                node_ids.append(node_id)

                time_elapsed(start_time, 'insert node')
            else:
                print('[-]Node is already in the network.')

        elif (choice == '2'):
            # search for data in the network
            query = input('[->]Search data: ')
            start_time = time.time()

            chord_net.find_data(query)
            time_elapsed(start_time, 'search data')

        elif (choice == '3'):
            # insert data to network
            query = input('[->]Enter data: ')
            start_time = time.time()

            chord_net.insert_data(query)

            time_elapsed(start_time, 'insert data')

        elif (choice == '4'):
            # print network graph
            if(len(chord_net.nodes) > 0):
                chord_net.print_network()

        elif (choice == '5'):
            # print network stats
            print(chord_net)

        elif (choice == '6'):
            node_id = int(input('[->]Enter node you wish to delete: '))

            node_ids.remove(node_id)

            start_time = time.time()

            chord_net.delete_node(node_id)

            time_elapsed(start_time, 'delete node')

        elif (choice == '7'):
            sys.exit(0)

        print('\n')


def create_network():
    sys.setrecursionlimit(10000000)

    ascii_banner = pyfiglet.figlet_format('CHORD')
    print(ascii_banner)
    print('Developed by: Konstantinos Bourantas[23 6145]')
    print('---------------------------------------------')

    m_par = int(input('Enter m parameter: '))
    Node.m = m_par
    Node.ring_size = 2 ** m_par

    print(f'Creating network with total capacity {Node.ring_size} nodes.')
    num_nodes = int(input('Enter number of nodes: '))

    while(num_nodes > 2**m_par):
        print('[-]Numbers of nodes cant be bigger than ring size.')
        num_nodes = int(input('Enter number of nodes : '))

    num_data = int(input('Number of fake data to be inserted: '))

    print('--------------------------------------------')

    node_ids = sample(range(Node.ring_size), num_nodes)

    chord_net = Network(m_par, node_ids)

    start_time = time.time()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        created_nodes = executor.map(
            chord_net.create_node, node_ids, chunksize=100)
        for node in created_nodes:
            chord_net.nodes.append(node)

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

    if(num_data > 0):
        chord_net.generate_fake_data(num_data)

    # Train the GNN model here using historical data
    chord_net.train_gnn_model()
    measure_performance(chord_net, node_ids)


    # show_menu(chord_net, node_ids)


if __name__ == '__main__':
    create_network()
