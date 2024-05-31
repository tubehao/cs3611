import random
import numpy as np
import Node
import hashlib

ip = "127.0.0.1"
m = 7
def nodeInf(port, ip = "127.0.0.1"):
    return ip + "|" + str(port) 

def hash(message):
    digest = hashlib.sha256(message.encode()).hexdigest()
    digest = int(digest, 16) % pow(2, m)
    return digest 

def nodeMessageProcessor(ip, port, message):
    # from chord import Chord
    from chord import ring
    print(ring)
    print(hash(str(nodeInf(port, ip))))
    receiveNode = ring[hash(str(nodeInf(port, ip)))]
    response = receiveNode.serve_requests(message)
    return response