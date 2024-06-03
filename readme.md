# CS3611 Big Homework: P2P with Chord

## Simulation

Logical layer simulation of the Chord protocol.

### Environment

- Python 3.8+
- torch
- pydotplus
- pyfiglet
- random
- hashlib

### Network.py

Implements basic network functions such as node joining and data lookup.

### Node.py

Implements basic node functionality, including searching and maintaining the Finger Table. Optimization schemes are implemented in the corresponding Python files based on Node.py.

### Usage

Run `python main.py` in the directory and follow the prompts to test basic functionality.

Run `python test.py -node Node -Net Network -n initial_node_count -m ring_size -f number_of_imported_virtual_data -dir directory_to_store_logs` in the directory for large-scale testing.

Parameter settings are shown in the table below:

| Plan                   | -node                    | -Net                        |
| ---------------------- | ------------------------ | --------------------------- |
| Baseline               | Node                     | Network                     |
| Dynamic Finger Updates | Node                     | dynamicFinerUpdateNetwork   |
| Enhanced Hashing       | SimpleOptimizationNode   | simpleOptimizationNetwork   |
| Hot Key Prioritization | hotKeyPrioritizationNode | hotKeyPrioritizationNetwork |
| PMLR                   | linearNode               | linearNetwork               |
| LSTM                   | lstmNode                 | lstmNetwork                 |

## Implementation

Implemented the Chord protocol based on explicit connections, but due to device limitations, it can only be tested on a small scale.

### Environment

- Python 3.10
- socket
- hashlib

### Node.py

Create a Node. Run Node.py on a computer using the following command to join the Chord network. When a new node other than the first one joins, the port of an already joined node needs to be provided.

+ Adding the first node:
    ```
    python Node.py yourPort
    ```
+ Adding other nodes:
    ```
    python Node.py yourPort anyAddedPort
    ```

### Client Access

Run the following command and follow the prompts to access the Node established on any port for searching, inserting, deleting, etc.

    python Client.py

For each data insertion, the information of the current lookup is automatically recorded in the log. The existing information in the log file is some experiments we have done.

## Visualization

### Environment

+ Node.js
+ npm
+ react

### Run

Input instruction to start:  

```
npm install react-scripts
npm start
```

If the prompt 'react scripts' is incorrect, it is not an internal or external command, nor is it a runnable program.

# Appendix

We completed our implementation based on the following two GitHub repositories:

https://github.com/Er-AbhishekRaj07/Chord-DHT-P2P-Network
https://github.com/omnone/CHORD-Simulation/blob/master
