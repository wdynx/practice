# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 01:21:51 2020

@author: wyx
"""


import requests
import re
import numpy as np
import datetime


r = requests.get('http://map.amap.com/service/subway?_1469083453978&srhdata=1100_drw_beijing.json')
text=r.text



def get_lines_stations_info(text):
    #正则表达式取所有的站名、路线以及是否为环线
    #站名信息元组第1，2个为坐标与站名，后两个为空
    #线路信息元组前两个位空，第3，4个为线路名与是否循环
    pattern=re.compile('(?:rs\":\"([0-9\s]+).*?\"n\":\"(.*?)\")|(?:ln\":\"(.*?)\".*?lo\":\"(.*?)\")')
    lines_list=pattern.findall(text)
    # 遍历text格式数据，组成地点数据结构
    # 所有线路信息的dict：key：线路名称；value：站点名称list
    lines_info = {}
    
    # 所有站点信息的dict：key：站点名称；value：站点坐标(x,y)
    stations_info = {}
    stationlist=[]
    
    
    for i in range(len(lines_list)):
        # 你可能需要思考的几个问题，获取「地铁线路名称，站点信息list，站名，坐标(x,y)，数据加入站点的信息dict，将数据加入地铁线路dict」
        if lines_list[i][-1]=='':
            stations_info[lines_list[i][1]]=tuple(map(int,lines_list[i][0].split(' ')))
            stationlist.append(lines_list[i][1])
        else:
            #将路线名与是否为环线拼接在一起，如：亦庄线0
            lines_info[lines_list[i][2]+lines_list[i][3]]=stationlist
            stationlist=[]
    return lines_info,stations_info

lines_info, stations_info = get_lines_stations_info(r.text)
#print(lines_info,stations_info)



# 根据线路信息，建立站点邻接表dict
def get_neighbor_info(lines_info):
    # 把str2加入str1站点的邻接表中
    def add_neighbor_dict(info, str1, str2):
        # 请在这里写代码
        if str1 not in info.keys():
            info[str1]=[]
        if str2 not in info.keys():
            info[str2]=[]
        info[str1].append(str2)
        info[str2].append(str1)
        
    neighbor_info={}
    for item in lines_info.items():
        for i in range(len(item[1])-1):
            add_neighbor_dict(neighbor_info,item[1][i],item[1][i+1])
        #若是环线，要考虑首尾的情况
        if item[0][-1]=='1':
            add_neighbor_dict(neighbor_info,item[1][0],item[1][-1])
            
    return neighbor_info
        
neighbor_info = get_neighbor_info(lines_info)
#print(neighbor_info)



# 画地铁图
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

# 如果汉字无法显示，请参照
matplotlib.rcParams['font.sans-serif'] = ['SimHei'] 
# matplotlib.rcParams['font.family']='sans-serif'
subwayMap=nx.Graph(neighbor_info)
fig=plt.figure(figsize=(24,16))
#原点在左上角
ax = plt.gca()                       #获取到当前坐标轴信息
ax.xaxis.set_ticks_position('top')   #将X坐标轴移到上面
ax.invert_yaxis()                    #反转Y坐标轴
nx.draw_networkx_nodes(subwayMap,pos=stations_info)
nx.draw_networkx_edges(subwayMap,pos=stations_info)
nx.draw_networkx_labels(subwayMap,pos=stations_info)
plt.show()



# 你可以用递归查找所有路径
def get_path_DFS_ALL(lines_info, neighbor_info, from_station, to_station):
    # 递归算法，本质上是深度优先
    # 遍历所有路径
    # 这种情况下，站点间的坐标距离难以转化为可靠的启发函数，所以只用简单的DFS算法
    # 检查输入站点名称
    res=get_next_station_DFS_ALL([{from_station},-1,[from_station]],neighbor_info,to_station)
    return res[-1]

def get_next_station_DFS_ALL(node, neighbor_info, to_station):
    res=[]
    #已知最短路径剪枝
    if node[1]!=-1 and len(node[-1])>node[1]:
        return res
    #图的直径
    if len(node[0])>54:
        return res
    if node[-1][-1]==to_station:
        node[1]=len(node[-1])
        return [node[-1].copy()]
    nextStations=neighbor_info[node[-1][-1]]
    for station in nextStations:
        if station not in node[0]:
            node[0].add(station)
            node[-1].append(station)
            res.extend(get_next_station_DFS_ALL(node,neighbor_info,to_station))
            node[0].remove(station)
            node[-1].pop()
    return res
start=datetime.datetime.now()
res=get_path_DFS_ALL(lines_info,neighbor_info, '奥体中心', '天安门东')
end=datetime.datetime.now()
print("DFS:",res)
print("用时：",end-start)



#  你也可以使用第二种算法：没有启发函数的简单宽度优先

def get_path_BFS(lines_info, neighbor_info, from_station, to_station):
    # 搜索策略：以站点数量为cost（因为车票价格是按站算的）
    # 这种情况下，站点间的坐标距离难以转化为可靠的启发函数，所以只用简单的BFS算法
    # 由于每深一层就是cost加1，所以每层的cost都相同，算和不算没区别，所以省略
    # 检查输入站点名称
    reached=[{from_station}]
    rnd=0
    #正向搜索
    while to_station not in reached[-1]:
        rnd+=1
        newset=set()
        for station in reached[-1]:
            newset|=set(neighbor_info[station])
        reached.append(newset)
    #反向寻找路径
    for i in range(len(reached)-1,-1,-1):
        if i==len(reached)-1:
            reached[i]=to_station
        else:
            for station in reached[i]:
                if station in neighbor_info[reached[i+1]]:
                    reached[i]=station
                    break
    return reached
        
start=datetime.datetime.now()
res=get_path_BFS(lines_info,neighbor_info,'奥体中心', '天安门东')
end=datetime.datetime.now()
print('BFS:',res)
print("用时：",end-start)

# 你还可以用第三种算法：以路径路程为cost的启发式搜索

import pandas as pd
def distance(stations_info,from_station,to_station):
    x=stations_info[from_station][0]-stations_info[to_station][0]
    y=stations_info[from_station][1]-stations_info[to_station][1]
    return (x**2+y**2)**0.5
    
def get_path_Astar(lines_info, neighbor_info, stations_info, from_station, to_station):
    # 搜索策略：以路径的站点间直线距离累加为cost，以当前站点到目标的直线距离为启发函数
    # 检查输入站点名称
    
    #预估每个点到终点的距离，放在字典中不用反复计算
    guessDic={}
    for station in neighbor_info.keys():
        guessDic[station]=distance(stations_info,station,to_station)
    #已确定的点
    reached={from_station:[0,0]}
    #备选的点、距离、上一个点
    neighbor={station:[distance(stations_info, from_station, station),from_station] for station in neighbor_info[from_station]}
    while to_station not in reached.keys():
        #找到去该点距离+预估距离最短的点
        bestItem=None
        bestDistance=10000
        for item in neighbor.items():
            if item[1][0]+guessDic[item[0]]<bestDistance:
                bestDistance=item[1][0]+guessDic[item[0]]
                bestItem=item
        reached[bestItem[0]]=bestItem[1]
        neighbor.pop(bestItem[0])
        for station in neighbor_info[bestItem[0]]:
            if station not in reached.keys():
                if station not in neighbor:
                    neighbor[station]=[bestItem[1][0]+distance(stations_info,bestItem[0],station),bestItem[0]]
                else:
                    curDistance=bestItem[1][0]+distance(stations_info,bestItem[0],station)
                    if curDistance<neighbor[station][0]:
                        neighbor[station]=[curDistance,bestItem[0]]
    #反向找路径
    path=[to_station]
    while path[-1]!=from_station:
        path.append(reached[path[-1]][-1])
    path.reverse()
    return path 

start=datetime.datetime.now()
res=get_path_Astar(lines_info, neighbor_info, stations_info, '奥体中心', '天安门东')
end=datetime.datetime.now()
print('Astar:',res)
print("用时：",end-start)
