import subprocess
import socket
import time

def is_port_in_use(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    except ConnectionRefusedError as e:
        print(f"Error checking port {port}: {e}")
        return False

def find_available_port(starting_port):
    port = starting_port
    while is_port_in_use(port):
        port += 1
    return port

def wait_for_port(port, timeout=60):
    """Wait until a port is accepting connections (TCP) or timeout is reached."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not is_port_in_use(port):
            time.sleep(1)
            continue
        return True
    return False

def wait_for_node_ready(ip, port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.close()
                return True
        except socket.error:
            time.sleep(0.5)
    return False

def create_chord_ring(node_count, starting_port):
    nodes = []
    ip = "127.0.0.1"
    for i in range(node_count):
        if i == 0:
            # First node
            port = find_available_port(starting_port)
            command = ["python", "Node.py", str(port)]
            subprocess.Popen(command)
            if not wait_for_node_ready(ip, port):
                print(f"Error: Node at port {port} did not start within the timeout period.")
                return []
            nodes.append(port)
        else:
            # Subsequent nodes
            known_port = nodes[0]
            port = find_available_port(starting_port)
            command = ["python", "Node.py", str(port), str(known_port)]
            subprocess.Popen(command)
            if not wait_for_node_ready(ip, port):
                print(f"Error: Node at port {port} did not start within the timeout period.")
                return []
            nodes.append(port)
        starting_port = port + 1
        time.sleep(2)
    return nodes


if __name__ == "__main__":
    node_count = int(input("Enter the number of nodes in the Chord ring: "))
    starting_port = 60000
    nodes = create_chord_ring(node_count, starting_port)
    print(f"Created Chord ring with nodes on ports: {nodes}")
