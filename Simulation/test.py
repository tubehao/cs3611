import hashlib
import os
import sys
import concurrent.futures
import time
import threading
import random
import pyfiglet
import argparse


def measure_performance(chord_net, node_ids, num_trials=50, log_dir='./log'):
    """
    Measure the performance of insert and search operations in the Chord network.
    Args:
        chord_net (Network): The Chord network instance.
        node_ids (list): List of node IDs in the network.
        num_trials (int): Number of trials for each operation.
        log_dir (str): Directory to store the log files.
    """
    results_insert = []
    results_search = []
    for num_nodes in [10, 50, 100, 500, 1000, 2000, 5000]:  
        print(f'\nTesting with {num_nodes} nodes...')
        results_insert = []  
        results_search = []  
        node_ids = random.sample(range(Node.ring_size), num_nodes)
        chord_net = Network(Node.m, node_ids)
        for node_id in node_ids:
            chord_net.insert_node(node_id)
        inserted_data = []  
        for _ in range(num_trials):
            data = str(random.choice(range(10000)))  
            start_time = time.time()
            hops_insert = chord_net.insert_data(data)
            results_insert.append(hops_insert)  
            inserted_data.append(data)  
        for data in inserted_data:
            num_searches = random.choice(range(5, 10))  
            for _ in range(num_searches):
                start_time = time.time()
                hops_search = chord_net.find_data(data)
                results_search.append(hops_search)  
        average_hops_insert = sum(results_insert) / len(results_insert)
        average_hops_search = sum(results_search) / len(results_search)
        with open(os.path.join(log_dir, f"logNode{args.node}Network{args.Net}.txt"), 'a') as file:
            file.write(f"Number of Nodes: {num_nodes}\n")
            file.write(f"Average Hops (Insert): {average_hops_insert}\n") 
            file.write(f"Average Hops (Search): {average_hops_search}\n")
            file.write(f"Number of Trials: {num_trials}\n\n")
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chord Network Performance Measurement')
    parser.add_argument('-node', type=str, default='Node', help='Node class name')
    parser.add_argument('-Net', type=str, default='Network', help='Network class name')
    parser.add_argument('-n', type=int, default=5000, help='Number of nodes')
    parser.add_argument('-m', type=int, default=22, help='Ring size (m)')
    parser.add_argument('-t', type=int, default=50, help='Number of trials')
    parser.add_argument('-dir', type=str, default='./log', help='Directory to store logs')
    args = parser.parse_args()
    Node = getattr(__import__(args.node), 'Node') 
    Network = getattr(__import__(args.Net), 'Network')
    Node.m = args.m
    Node.ring_size = 2 ** args.m
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
    node_ids = random.sample(range(Node.ring_size), args.n)
    chord_net = Network(args.m, node_ids)
    measure_performance(chord_net, node_ids, num_trials=args.t, log_dir=args.dir)
