import random
import numpy as np
import Node
import hashlib

from utils import *
    



ring = {}

def addNode(port, ExistingNodePort):
    node = Node.Node(ip, int(port))
    # print(hash(str(nodeInf(port, ip))) == node.id)

    if ring == {}:
        print("creating chord")
        ring[node.id] = node
        node.predecessor = node
        node.successor = node

        node.finger_table.table[0][1] = node
        node.start()
        print("Node added to chord")
        # print(ring)
        return
    elif ring.get(hash(nodeInf(ExistingNodePort))) == None:
        print("Existing node does not exist")
        return
    elif ring.get(hash(nodeInf(port))) == None:
        node.join(ip, ExistingNodePort)
        node.start()
        ring[node.id] = node
        print("Node added to chord")
        return
    else :
        print("Node already exists")
        return

def deleteNode(port):
    leavingNode = ring[hash(nodeInf(port))]
    leavingNode.leave()
    del ring[hash(str(nodeInf(port)))]

def leaveChord():
    for node in ring.values():
        node.leave()

def enterNode(port, ip = "127.0.0.1"):
    nodeId = hash(str(nodeInf(port, ip)))
    if ring.get(nodeId) == None:
        print("Node does not exist")
        return
    else:
        node = ring[nodeId]
        display(node)
        return

def display(node):
    print("Node id : ", node.id)
    print("Node ip : ", node.ip)
    print("Node port : ", node.port)
    print("Node predecessor : ", node.predecessor.id)
    print("Node successor : ", node.successor.id)
    print("Node finger table : ", node.finger_table.table)
    while(True):
        print("************************MENU*************************")
        print("PRESS ***********************************************")
        print("1. TO ENTER *****************************************")
        print("2. TO SHOW ******************************************")
        print("3. TO DELTE *****************************************")
        print("0. TO EXIT ******************************************")
        print("*****************************************************")
        choice = input()


        if(choice == '1'):
            key = input("ENTER THE KEY : ")
            val = input("ENTER THE VALUE : ")
            message = "insert|" + str(key) + ":" + str(val)
            
            data = nodeMessageProcessor(node, node.ip, node.port, message)
            print(data)

        elif(choice == '2'):
            key = input("ENTER THE KEY")
            message = "search|" + str(key)
            data = nodeMessageProcessor(node, node.ip, node.port, message)
            
            print("The value corresponding to the key is : ",data)

        elif(choice == '3'):
            key = input("ENTER THE KEY")
            message = "delete|" + str(key)
            data = nodeMessageProcessor(node, node.ip, node.port, message)
            print(data)

        elif(choice == '0'):
            print("Exiting Node")
            exit()
            
        else:
            print("INCORRECT CHOICE")

def sendMessagefromChord(port, message):
    node = ring[hash(str(nodeInf(port)))]
    response = node.serve_requests(message)
    return response

if __name__ == "__main__":
    while(True):
        print(ring)
        print("************************MENU*************************")
        print("PRESS ***********************************************")
        print("1. Add a node *****************************************")
        print("2. Delete a node ******************************************")
        print("3. Enter a node *****************************************")
        print("0. EXIT ******************************************")
        print("*****************************************************")
        choice = input()

        if(choice == '1'):
            port = input("ENTER THE port : ")
            ExistingNodePort = None
            if ring != {}:
                ExistingNodePort = input("ENTER THE EXISTING NODE PORT (if any): ")
            addNode(port, ExistingNodePort)
            # print(f"Add node id {id} to the chord")
            continue

        elif(choice == '2'):
            port = input("ENTER THE port : ")
            deleteNode(port)
            print(f"Node with port {port} has been deleted")
            continue

        elif(choice == '3'):
            enterNode(input("ENTER THE port : "))
            continue

        elif(choice == '0'):
            print("bye~")
            exit()
            
        else:
            print("INCORRECT CHOICE")
            continue

# def nodeMessageProcessor(chord,ip, port, message):
#     print(ring)
#     print(hash(str(nodeInf(port, ip))))
#     receiveNode = ring[hash(str(nodeInf(port, ip)))]
#     response = receiveNode.serve_requests(message)
#     return response
        
