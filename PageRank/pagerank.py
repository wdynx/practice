# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 12:35:29 2020

@author: wyx
"""


import networkx as nx
import itertools
import matplotlib.pyplot as plt
import random
import numpy as np

graph=nx.DiGraph()
graph.add_nodes_from(['A','B','C','D','E','F'])
graph.add_edges_from([('A','B'),('A','D'),('A','F'),('B','C'),('C','E'),
                      ('D','A'),('D','C'),('D','E'),('E','B'),('E','C'),
                      ('F','D')])
layout=nx.circular_layout(graph)
nx.draw(graph,pos=layout,with_labels=True,hold=False)
plt.show()

print('调用networkx方法：')
print('简化模型：')
simplePR=nx.pagerank(graph,alpha=1)
for point in simplePR.items():
    print(point)
print('随机模型：')
randomPR=nx.pagerank(graph,alpha=0.85)
for point in randomPR.items():
    print(point)
print('---------------------------------')

def myPageRank(graph,alpha=1,maxiter=100):
    nodesCount=len(graph.nodes)
    nodesValue=np.full((nodesCount,1),1/nodesCount)
    nodesPR=np.zeros((nodesCount,nodesCount),dtype=float)
    nodesDic={}
    index=0
    for node in graph.nodes:
        nodesDic[node]=index
        index+=1
    for node in graph.nodes:
        neighborCount=graph.out_degree(node)
        for neighbor in graph.neighbors(node):
            nodesPR[nodesDic[neighbor],nodesDic[node]]=1/neighborCount
    for i in range(100):
        nodesValue=alpha*nodesPR.dot(nodesValue)+1-alpha
    returnDic={}
    for i in range(nodesCount):
        returnDic[list(graph.nodes)[i]]=nodesValue[i,0]
    return returnDic

print('手动实现PageRank：')
print('简化模型：')
mySimplePR=myPageRank(graph)
for point in mySimplePR.items():
    print(point)
print('随机模型：')
myRandomPR=nx.pagerank(graph,alpha=0.85)
for point in myRandomPR.items():
    print(point)
