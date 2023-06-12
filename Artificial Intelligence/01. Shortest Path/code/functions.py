from source import *
# 判断图是否建成，请直接运行该文件

CitiesToFetch = []
def DataProcessing():
    global CitiesToFetch
    enum, vnum = 0, 0
    input_data = []

    f = open("Romania.txt", 'r')
    lst = f.read().split('\n')
    f.close()
    for item in lst:
        temp = item.split(' ')
        if len(temp) == 2:
            vnum = int(temp[0])
            enum = int(temp[1])
        elif len(temp) == 3:
            input_data.append(temp)
            CitiesToFetch.extend(temp[:2])
    CitiesToFetch = list(set(CitiesToFetch))
    return vnum, enum, input_data

def GraphInit():
    (vnum, enum, edges) = DataProcessing()
    graph = Graph(vnum, CitiesToFetch)
    for edge in edges:
        graph.AddEdge(edge[0], edge[1], int(edge[2]))


    if __name__ == '__main__':
        #检查图是否成功构造
        for ii in graph.adj.items():
            print(ii[0] + ':', end='\n                  ')
            for edge in ii[1].edgeList:
                print(edge.PrintStr(), end=' ')
            print()


    return graph

# 对用户的输入进行模糊匹配
def CityMatch(cityToMatch: str):
    if cityToMatch[len(cityToMatch) - 1] == ',':
        cityToMatch = cityToMatch[:len(cityToMatch) - 1]
    for city in CitiesToFetch:
        if len(cityToMatch) > len(city):
            continue
        else:
            for length in range(1, len(city) + 1):
                sub = city[:length]
                if sub == cityToMatch:
                    return city
    return 'false'




if __name__ == '__main__':
    print('生成的无向图邻接表如下：')
    temp = GraphInit()