# CS3611 Big Homework: P2P with Chord

## Simulation

Chord协议的简单模拟。

### Enviroment

- Python 3.8+
- torch
- pydotplus
- pyfiglet
- random

### Network.py 

实现了基本的节点的加入，数据查找等网络功能。

### Node.py

实现了基本的node节点的功能，包括查找和维护Finger Table，添加的功能基于Node.py实现在对应名称的python文件中。

### 使用方式

在目录下运行`python main.py`，根据提示菜单输入，可以进行基本的功能的测试。

在目录下运行`python test.py -node Node -Net Network -n 初始节点数目 -m 环的大小 -f 导入的虚拟数据的数目 -dir 存储日志的目录`，测试代码。

## Implementation

实现了基于显示连接的Chord协议，但是由于计算机设备限制，只能在小规模下测试。

### Enviroment

- Python 3.8+
- torch
- pydotplus
- pyfiglet
- random

### Node.py

建立一个Node，在计算机下通过下述命令运行Node.py，则就是将本机加入了Chord网络，当非第一个的新节点加入时，需要给出一个已加入的节点的端口。

+ 添加第一个节点：
    ```
    python Node.py port1
    ```
+ 添加其他节点：
    ```
    python Node.py anyAddedPort
    ```

### 客户端访问：

通过运行下述命令，根据提示输入即可访问建立在任意端口的Node，进行查找插入删除等工作。

    python Client.py

对于每一次插入数据，自动在log中记录本次查找的信息，log文件中已有的是我们做的一些实验。

## Visualization

### Environment

+ Node.js

+ npm

+ react

### Run

 Input instruction: 

```
npm install react-scripts
npm start
```

(if the prompt 'react scripts' is incorrect, it is not an internal or external command, nor is it a runnable program)



