from source import *


def init():
    edges = []
    vertex_list = set()
    (m, n) = input().split()
    for ii in range(int(n)):
        (start, end, weight) = input().split()
        vertex_list.update({start, end})
        edges.append([start, end, int(weight)])
    return edges, list(vertex_list)


(edges, vertex_list) = init()
graph = Graph(len(vertex_list), vertex_list)
for edge in edges:
    graph.AddEdge(edge[0], edge[1], edge[2])
(st, ed) = input().split()
solution = Dijkstra(graph, st)
print('----------------------')
print(solution.DistanceTo(ed))
print('->'.join(solution.PathTo(ed)))


'''
a b 2
a c 3
b d 5
b e 2
c e 5
d e 1
d z 2
e z 4
'''