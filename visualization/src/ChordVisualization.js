import React, { useState, useEffect } from 'react';
import * as d3 from 'd3';
import './App.css';  // 引入 CSS 文件

const m = 6;  // 定义 m 位标识符空间大小
const totalNodes = Math.pow(2, m);  // 环上的总点数
const radiusOffset = 30; // 环外的偏移半径

const ChordVisualization = () => {
  const [nodes, setNodes] = useState(Array(totalNodes).fill(null));
  const [queries, setQueries] = useState([]);
  const [data, setData] = useState([]);  // 存储数据的状态
  const svgRef = React.useRef();

  useEffect(() => {
    drawChord();
  }, [nodes, data]);

  const [sourceNode, setSourceNode] = useState('');
  const [targetNode, setTargetNode] = useState('');
  const [routePath, setRoutePath] = useState([]);

  const handleRouting = () => {
    const source = parseInt(sourceNode);
    const target = parseInt(targetNode);
  
    // 检查源节点和目标节点是否存在
    const sourceNodeExists = nodes.some(node => node && node.id === source);
    const targetNodeExists = nodes.some(node => node && node.id === target);
  
    if (!sourceNodeExists || !targetNodeExists) {
      alert("源节点或目标节点不存在，请输入有效的节点ID。");
      return;
    }
  
    // 执行路由寻址逻辑
    const route = findRoute(source, target);
    setRoutePath(route);
  
    // 重新绘制Chord图
    drawChord();
  };

  const generateRandomIp = () => {
    return `${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}`;
  };

  const generateRandomHeader = () => {
    return Math.random().toString(36).substring(2, 10);  // 生成一个随机字符串作为数据报头
  };

  const hashIpToId = (ip) => {
    return parseInt(ip.split('.').reduce((acc, octet) => acc + octet, ''), 10) % totalNodes;
  };

  const hashKey = (key) => {
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
      const char = key.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash) % totalNodes;
  };

  const addNode = () => {
    const ip = generateRandomIp();
    const nodeId = hashIpToId(ip);
    const newNodes = [...nodes];
    newNodes[nodeId] = { id: nodeId, ip };
    setNodes(newNodes);
    drawChord();
  };

  const removeNode = (id) => {
    const newNodes = [...nodes];
    const successorNode = findSuccessor(id);
    
    // Transfer data to successor node
    if (successorNode) {
      const newData = data.map(d => {
        if (d.node.id === id) {
          return { ...d, node: successorNode };
        }
        return d;
      });
      setData(newData);
    }
    
    newNodes[id] = null;
    setNodes(newNodes);
    drawChord();
  };

  const findSuccessor = (start) => {
    // 查找大于或等于start的最小节点
    for (let i = start; i < totalNodes; i++) {
      if (nodes[i]) {
        return nodes[i];
      }
    }
    // 如果没有找到，查找最小的节点作为后继节点
    for (let i = 0; i < start; i++) {
      if (nodes[i]) {
        return nodes[i];
      }
    }
    return null;
  };

  const findNodeForKey = (keyHash) => {
    for (let i = keyHash; i < totalNodes; i++) {
      if (nodes[i]) {
        return nodes[i];
      }
    }
    for (let i = 0; i < keyHash; i++) {
      if (nodes[i]) {
        return nodes[i];
      }
    }
    return null;
  };

  const uploadData = () => {
    const header = generateRandomHeader();
    const keyHash = hashKey(header);
    const node = findNodeForKey(keyHash);
    if (node) {
      setData(prevData => [...prevData, { key: keyHash, keyHash, node }]);  // 存储哈希后的key值
    } else {
      alert('No node available to store the data.');
    }
  };

  const showFingerTable = (node) => {
    if (!node) return;

    const fingerTableContainer = d3.select("#finger-table-container");
    fingerTableContainer.selectAll("*").remove();

    const fingerTable = getFingerTable(node.id);

    const containerWidth = 300;
    const containerHeight = (fingerTable.length + 1) * 20 + 20;

    fingerTableContainer.append("rect")
      .attr("x", -containerWidth / 2)
      .attr("y", -containerHeight / 2)
      .attr("width", containerWidth)
      .attr("height", containerHeight)
      .attr("fill", "white")
      .attr("stroke", "black")
      .attr("stroke-width", 1)
      .attr("rx", 5)
      .attr("ry", 5);

    fingerTableContainer.append("text")
      .attr("x", -containerWidth / 2 + 10)
      .attr("y", -containerHeight / 2 + 10)
      .attr("dy", "1em")
      .attr("font-size", "14px")
      .attr("font-family", "'Roboto', sans-serif")
      .attr("fill", "black")
      .text(`Finger Table for Node ${node.id}`);

    fingerTable.forEach((entry, index) => {
      fingerTableContainer.append("text")
        .attr("x", -containerWidth / 2 + 10)
        .attr("y", -containerHeight / 2 + (index + 2) * 20)
        .attr("dy", "1em")
        .attr("font-size", "12px")
        .attr("font-family", "'Roboto', sans-serif")
        .attr("fill", "black")
        .text(`Start: ${entry.start}, Interval: [${entry.start}, ${entry.end}), Successor: ${entry.successor}`);
    });
  };

  const hideFingerTable = () => {
    d3.select("#finger-table-container").selectAll("*").remove();
  };

  const getFingerTable = (nodeId) => {
    const fingerTable = [];
    for (let i = 0; i < m; i++) {
      const start = (nodeId + Math.pow(2, i)) % totalNodes;
      const end = (nodeId + Math.pow(2, i + 1)) % totalNodes;
      const successor = findSuccessor(start);
      fingerTable.push({
        start,
        end,
        successor: successor ? successor.id : "None"
      });
    }
    return fingerTable;
  };

  const findRoute = (source, target) => {
    const path = [];
    let currentNode = nodes[source];

    while (currentNode.id !== target) {
      path.push(currentNode.id);
      const fingerTable = getFingerTable(currentNode.id);
      let nextNode = fingerTable.find(f => f.start <= target && target < f.end);
      if (!nextNode) {
        nextNode = fingerTable[fingerTable.length - 1];
      }
      currentNode = nodes[nextNode.successor];
    }

    path.push(target);
    return path;
  };
  
  const drawChord = () => {
    const width = 600;
    const height = 600;
  
    // 清空之前的绘图
    d3.select(svgRef.current).selectAll("*").remove();
  
    // 创建SVG容器
    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", `translate(${width / 2},${height / 2})`);
  
    const arc = d3.arc()
      .innerRadius(200)
      .outerRadius(220);
  
    const pie = d3.pie()
      .sort(null)
      .value(1);
  
    const nodeData = nodes.map((node, i) => ({
      id: i,
      node,
      startAngle: i * 2 * Math.PI / totalNodes,
      endAngle: (i + 1) * 2 * Math.PI / totalNodes
    }));
  
    const arcs = svg.selectAll(".arc")
      .data(pie(nodeData))
      .enter().append("g")
      .attr("class", "arc");
  
    arcs.append("circle")
      .attr("transform", d => {
        const angle = (d.startAngle + d.endAngle) / 2;
        return `translate(${Math.cos(angle) * 200},${Math.sin(angle) * 200})`;
      })
      .attr("r", 15)
      .attr("fill", "#2C3E50")
      .on("mouseover", function (event, d) {
        d3.select(this).attr("fill", "orange");
        showFingerTable(d.data.node); // 显示路由表
      })
      .on("mouseout", function (event, d) {
        d3.select(this).attr("fill", "#2C3E50");
        hideFingerTable(); // 隐藏路由表
      });
  
    arcs.append("text")
      .attr("transform", d => {
        const angle = (d.startAngle + d.endAngle) / 2;
        return `translate(${Math.cos(angle) * 200},${Math.sin(angle) * 200})`;
      })
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .attr("font-size", "12px")
      .attr("font-family", "'Roboto', sans-serif")
      .attr("fill", "white")
      .text(d => d.data.node ? d.data.node.id : '');
  
    // 绘制数据报的圆圈和箭头
    nodes.forEach((node, nodeIndex) => {
      if (node) {
        const angle = (nodeIndex + 0.5) * 2 * Math.PI / totalNodes;
        const xNode = Math.cos(angle) * 200;
        const yNode = Math.sin(angle) * 200;
  
        data.filter(d => d.node.id === node.id).forEach((d, i) => {
          const offsetAngle = angle + (Math.random() * 0.2 - 0.1) * Math.PI; // 数据报圆圈随机分布在节点外侧
          const offsetRadius = 230; // 数据报圆圈与节点的固定距离
          const xData = Math.cos(offsetAngle) * offsetRadius;
          const yData = Math.sin(offsetAngle) * offsetRadius;
  
          // 绘制数据键的圆圈
          svg.append("circle")
            .attr("transform", `translate(${xData},${yData})`)
            .attr("r", 10)
            .attr("fill", "yellow");
  
          // 显示数据键
          svg.append("text")
            .attr("transform", `translate(${xData},${yData})`)
            .attr("dy", "0.35em")
            .attr("text-anchor", "middle")
            .attr("font-size", "10px")
            .attr("font-family", "'Roboto', sans-serif")
            .attr("fill", "black")
            .text(d.key);
  
          // 绘制指向节点的箭头
          svg.append("line")
            .attr("x1", xData)
            .attr("y1", yData)
            .attr("x2", xNode)
            .attr("y2", yNode)
            .attr("stroke", "yellow")
            .attr("stroke-width", 2)
            .attr("marker-end", "url(#arrow)");
        });
      }
    });
  
    // 创建路径绘制层
    if (routePath.length > 1) {
      const lineGenerator = d3.line().curve(d3.curveBasis);
      const pathData = routePath.map(nodeId => {
        const angle = (nodeId + 0.5) * 2 * Math.PI / totalNodes;
        return [Math.cos(angle) * 200, Math.sin(angle) * 200];
      });
  
      pathData.forEach((pos, i) => {
        if (i < pathData.length - 1) {
          svg.append("line")
            .attr("x1", pos[0])
            .attr("y1", pos[1])
            .attr("x2", pathData[i + 1][0])
            .attr("y2", pathData[i + 1][1])
            .attr("stroke", "red")
            .attr("stroke-width", 2)
            .attr("marker-end", "url(#arrow)");
  
          svg.append("circle")
            .attr("cx", pos[0])
            .attr("cy", pos[1])
            .attr("r", 5)
            .attr("fill", "red");
        }
      });
    }
  
    // 设置路由表的SVG容器
    svg.append("g")
      .attr("id", "finger-table-container")
      .attr("transform", "translate(0, 0)"); // 确保路由表在圆环中心
  };
  
  
  
  const handleInputChange = (setter) => (e) => {
    const value = e.target.value;
    if (!isNaN(value) && Number.isInteger(Number(value))) {
      setter(value);
    }
  };
  
  return (
    <div className="app-container">
      <div id="chord-container">
        <svg ref={svgRef}></svg>
      </div>
      <div className="controls">
        <button onClick={addNode}>Add Node</button>
        <button onClick={uploadData}>Upload Data</button>
      </div>
      <div className="routing-controls">
        <input
          type="number"
          placeholder="Source Node"
          value={sourceNode}
          onChange={handleInputChange(setSourceNode)}
          className="add-source-input"
        />
        <input
          type="number"
          placeholder="Target Node"
          value={targetNode}
          onChange={handleInputChange(setTargetNode)}
          className="find-input"
        />
        <button onClick={handleRouting} className="controls-button">Find Route</button>
      </div>
      <div className="node-list">
        <table>
          <thead>
            <tr>
              <th>Node ID</th>
              <th>IP Address</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {nodes.map((node, index) => (
              node && (
                <tr key={index}>
                  <td>{node.id}</td>
                  <td>{node.ip}</td>
                  <td>
                    <button onClick={() => removeNode(node.id)}>Remove</button>
                  </td>
                </tr>
              )
            ))}
          </tbody>
        </table>
      </div>
      <div className="data-list">
        <h3>Data Storage</h3>
        <table>
          <thead>
            <tr>
              <th>Data Key</th>
              <th>Stored at Node</th>
            </tr>
          </thead>
          <tbody>
            {data.map((d, index) => (
              d && d.node && (
                <tr key={index}>
                  <td>{d.key}</td>
                  <td>{d.node.id}</td>
                </tr>
              )
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
  
};

export default ChordVisualization;
