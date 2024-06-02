import numpy as np

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = np.zeros((state_size, action_size))

    def choose_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return np.random.randint(self.action_size)
        else:
            return np.argmax(self.q_table[state])

    def update_q_value(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error




class Node(object):
    m = 0
    ring_size = 2 ** m

    def __init__(self, node_id, m):
        self.node_id = node_id
        self.predecessor = self
        self.successor = self
        self.data = dict()
        self.fingers_table = [self]*m
        self.access_count = {}
        self.agent = QLearningAgent(state_size=m, action_size=m)
        self.state = self.node_id % m

    def __str__(self):
        return f'Node {self.node_id}'

    def __lt__(self, other):
        return self.node_id < other.node_id

    ################################################################################################################

    def record_access(self, key):
        if key in self.access_count:
            self.access_count[key] += 1
        else:
            self.access_count[key] = 1

    def get_reward(self, key):
        return self.access_count.get(key, 0)

    def fix_fingers(self):
        for i in range(self.m):
            action = self.agent.choose_action(self.state)
            reward = self.get_reward(action)
            next_state = (self.state + 1) % self.m
            self.agent.update_q_value(self.state, action, reward, next_state)
            self.fingers_table[i], _ = self.find_successor(self.node_id + 2 ** action)
            self.state = next_state

    def find_successor(self, key):
        if self.node_id == key:
            return self, 1
        if self.distance(self.node_id, key) <= self.distance(self.successor.node_id, key):
            self.record_access(key)
            return self.successor, 1
        next_node, path = self.closest_preceding_node(self, key).find_successor(key)
        self.record_access(key)
        return next_node, path+1

    def print_fingers_table(self):
        print(
            f'Node: {self.node_id} has Successor:{self.successor.node_id}  and Pred:{self.predecessor.node_id}')
        print('Finger Table:')
        for i in range(self.m):
            print(
                f'{(self.node_id + 2 ** i) % self.ring_size} : {self.fingers_table[i].node_id}')

    ################################################################################################################
    # Add  node to the network
    def join(self, node):
        # find nodes succesor in the network
        succ_node, path = node.find_successor(self.node_id)

        # find predecessor of successor
        pred_node = succ_node.predecessor

        # insert node in the right place on the network
        self.find_node_place(pred_node, succ_node)

        # fix fingers of inserted node
        self.fix_fingers()

        self.take_successor_keys()

    def leave(self):
        #fix succ and pred before leaving
        self.predecessor.successor = self.successor
        self.predecessor.fingers_table[0] = self.successor
        self.successor.predecessor = self.predecessor

        #pass key to successor
        for key in sorted(self.data.keys()):
            self.successor.data[key] = self.data[key]

    ################################################################################################################

    def find_node_place(self, pred_node, succ_node):
        pred_node.fingers_table[0] = self
        pred_node.successor = self

        succ_node.predecessor = self

        self.fingers_table[0] = succ_node
        self.successor = succ_node
        self.predecessor = pred_node

    def take_successor_keys(self):
        #take the keys from your succ that are >= node_id
        self.data = {key: self.successor.data[key] for key in sorted(
            self.successor.data.keys()) if key <= self.node_id}

        for key in sorted(self.data.keys()):
            if key in self.successor.data:
                del self.successor.data[key]

    ################################################################################################################


    ################################################################################################################
    # return closest preceding node
    def closest_preceding_node(self, node, hashed_key):

        for i in range(len(node.fingers_table)-1, 0, -1):
            if self.distance(node.fingers_table[i-1].node_id, hashed_key) < self.distance(node.fingers_table[i].node_id, hashed_key):
                return node.fingers_table[i-1]

        return node.fingers_table[-1]

    ################################################################################################################

    def distance(self, n1, n2):

        return n2-n1 if n1 <= n2 else self.ring_size - n1 + n2

    ################################################################################################################

    # Find the node responsible for the key
   
    ################################################################################################################
