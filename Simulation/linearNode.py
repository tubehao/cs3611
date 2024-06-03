import hashlib
import numpy as np
from sklearn.linear_model import LinearRegression
class Node(object):
    m = 11
    ring_size = 2 ** m
    def __init__(self, node_id, m):
        self.node_id = node_id
        self.predecessor = self
        self.successor = self
        self.data = dict()
        self.fingers_table = [self]*m
        self.access_count = {}
        self.access_history = {}
    def __str__(self):
        return f'Node {self.node_id}'
    def __lt__(self, other):
        return self.node_id < other.node_id
    def print_fingers_table(self):
        print(
            f'Node: {self.node_id} has Successor:{self.successor.node_id}  and Pred:{self.predecessor.node_id}')
        print('Finger Table:')
        for i in range(self.m):
            print(
                f'{(self.node_id + 2 ** i) % self.ring_size} : {self.fingers_table[i].node_id}')
    def record_access(self, key):
        if key in self.access_count:
            self.access_count[key] += 1
        else:
            self.access_count[key] = 1
        if key not in self.access_history:
            self.access_history[key] = []
        self.access_history[key].append(self.access_count[key])
    def predict_access(self, key):
        if key not in self.access_history or len(self.access_history[key]) < 2:
            return 0
        X = np.arange(len(self.access_history[key])).reshape(-1, 1)
        y = np.array(self.access_history[key])
        model = LinearRegression()
        model.fit(X, y)
        prediction = model.predict(np.array([[len(self.access_history[key])]]))[0]
        return prediction
    def join(self, node):
        succ_node, path = node.find_successor(self.node_id)
        pred_node = succ_node.predecessor
        self.find_node_place(pred_node, succ_node)
        self.fix_fingers()
        self.take_successor_keys()
    def leave(self):
        self.predecessor.successor = self.successor
        self.predecessor.fingers_table[0] = self.successor
        self.successor.predecessor = self.predecessor
        for key in sorted(self.data.keys()):
            self.successor.data[key] = self.data[key]
    def find_node_place(self, pred_node, succ_node):
        pred_node.fingers_table[0] = self
        pred_node.successor = self
        succ_node.predecessor = self
        self.fingers_table[0] = succ_node
        self.successor = succ_node
        self.predecessor = pred_node
    def take_successor_keys(self):
        self.data = {key: self.successor.data[key] for key in sorted(
            self.successor.data.keys()) if key <= self.node_id}
        for key in sorted(self.data.keys()):
            if key in self.successor.data:
                del self.successor.data[key]
    def fix_fingers(self):
        predictions = {}
        for key in self.access_count.keys():
            predictions[key] = self.predict_access(key)
        sorted_keys = sorted(predictions.keys(), key=lambda k: predictions[k], reverse=True)
        for i in range(1, len(self.fingers_table)):
            start = (self.node_id + 2 ** i) % self.ring_size
            end = (self.node_id + 2 ** (i + 1)) % self.ring_size
            print(f"Updating finger {i}, start: {start}, end: {end}")
            found = False
            for hot_key in sorted_keys:
                hot_key_hashed = hot_key
                if start < end:
                    if start < hot_key_hashed <= end:
                        self.fingers_table[i], _ = self.find_successor(hot_key_hashed)
                        print(f"Finger {i} updated to hot key {hot_key} with node {self.fingers_table[i].node_id}")
                        found = True
                        break
                else:
                    if start < hot_key_hashed or hot_key_hashed <= end:
                        self.fingers_table[i], _ = self.find_successor(hot_key_hashed)
                        print(f"Finger {i} updated to hot key {hot_key} with node {self.fingers_table[i].node_id}")
                        found = True
                        break
            if not found:
                self.fingers_table[i], _ = self.find_successor(start)
                print(f"Finger {i} updated to node {self.fingers_table[i].node_id}")
        print("finish fix finger")
    def closest_preceding_node(self, node, hashed_key):
        for i in range(len(node.fingers_table)-1, 0, -1):
            if self.distance(node.fingers_table[i-1].node_id, hashed_key) < self.distance(node.fingers_table[i].node_id, hashed_key):
                return node.fingers_table[i-1]
        return node.fingers_table[-1]
    def distance(self, n1, n2):
        return n2-n1 if n1 <= n2 else self.ring_size - n1 + n2
    def find_successor(self, key):
        if self.node_id == key:
            return self, 1
        if self.distance(self.node_id, key) <= self.distance(self.successor.node_id, key):
            self.record_access(key)
            return self.successor, 1
        next_node, path = self.closest_preceding_node(self, key).find_successor(key)
        self.record_access(key)
        return next_node, path+1
