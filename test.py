import subprocess
import time

# 初始节点的端口号
initial_port = 50000

# 创建初始节点
initial_process = subprocess.Popen(['python', 'Node.py', str(initial_port)])
time.sleep(2)  # 等待初始节点启动

# 添加 999 个新节点
processes = []
for i in range(1, 10):
    new_port = initial_port + i
    process = subprocess.Popen(['python', 'Node.py', str(new_port), str(initial_port)])
    processes.append(process)
    time.sleep(1)  # 等待新节点加入网络

time.sleep(400)

# 在这里结束所有子进程
for process in processes:
    process.terminate()

initial_process.terminate()

print("50 个节点已成功加入 Chord 网络")