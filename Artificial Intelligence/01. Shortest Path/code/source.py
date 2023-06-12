import sys
# a = np.loadtxt("D:/《学习资料》/大二下/人工智能/coding/实验一/Romania.txt")
# print(type(a), a, np.shape(a), sep='\n')

def IsFinish(pq: dict):
    for value in pq.values():
        if value != -1:
            return False
    return True


class Edge:
    def __init__(self, start: str = "null", end: str = "null", weight: int = 0):
        self.start = start
        self.end = end
        self.weight = weight

    def IsEmpty(self):
        return self.start == "null" and self.end == "null" and self.weight == 0

    def PrintStr(self):
        return '[' + self.start + ', ' + self.end + ', ' + str(self.weight) + ']'

class Vertex:
    def __init__(self, name):
        self.name = name
        self.edgeList = []


class Graph:
    def __init__(self, vertexNum: int, vertexNameList: list):
        self.vnum, self.enum = vertexNum, 0
        self.NameList = vertexNameList
        self.adj = {}
        for Name in self.NameList:
            self.adj[Name] = Vertex(Name)

    def AddEdge(self, st: str, ed: str, w: int):
        self.adj[st].edgeList.append(Edge(st, ed, w))
        self.adj[ed].edgeList.append(Edge(ed, st, w))
        self.enum += 1


class Dijkstra:
    def __init__(self, graph: Graph, start: str):
        self.check = ''
        self.DistTo = dict(zip(graph.NameList, [sys.maxsize] * len(graph.NameList)))
        self.EdgeTo = dict(zip(graph.NameList, [Edge()] * len(graph.NameList)))
        self.pq = dict(zip(graph.NameList, [-1] * len(graph.NameList)))

        self.DistTo[start], self.pq[start] = 0, 0
        while not IsFinish(self.pq):
            min, min_city = sys.maxsize, 0
            for key in self.pq.keys():
                if self.pq[key] != -1 and self.pq[key] < min:
                    min, min_city = self.pq[key], key
            self.pq[min_city] = -1
            self.relax(graph, min_city)

    def relax(self, graph: Graph, v: str):
        for edge in graph.adj[v].edgeList:
            if self.DistTo[v] + edge.weight < self.DistTo[edge.end]:
                self.DistTo[edge.end] = self.DistTo[v] + edge.weight
                self.EdgeTo[edge.end] = edge
                self.pq[edge.end] = self.DistTo[edge.end]

    def hasPathTo(self, ed: str):
        return self.DistTo[ed] != sys.maxsize

    def DistanceTo(self, ed: str):
        return self.DistTo[ed]

    def PathTo(self, ed: str):
        '''
        for key in self.EdgeTo.keys():
            print(key + ': [' + self.EdgeTo[key].start + ', ' + self.EdgeTo[key].end + ', ' + str(
                self.EdgeTo[key].weight) + ']')
        print(self.DistTo)
        '''
        path = []
        if not self.hasPathTo(ed):
            return path
        else:
            p = ed
            while True:
                path.append(self.EdgeTo[p].end)
                self.check += str(self.EdgeTo[p].weight)[::-1] + ' + '
                p = self.EdgeTo[p].start
                if self.EdgeTo[p].IsEmpty():
                    path.append(p)
                    self.check = self.check[:len(self.check) - 3][::-1]
                    return path[::-1]