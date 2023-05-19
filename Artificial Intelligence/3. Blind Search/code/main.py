import copy
import time

x_range, y_range = 0, 0
_path = []


class Node:
    x = None
    y = None
    val = None
    par = None

    def __init__(self, val: str, x=0, y=0):
        self.val = val
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __eq__(self, other):
        if type(other) == type(self) and self.x == other.x and self.y == other.y:
            return True
        else:
            return False


class Maze:
    maze = None
    marked = None
    arrived = False
    m1, m2 = None, None

    def __init__(self, maze: list):
        self.maze, self.marked = [], []
        for i in range(len(maze)):
            sub = ''
            maze_tmp = []
            for j in range(len(maze[i])):
                maze_tmp.append(Node(maze[i][j], j, i))
                sub += '1' if maze[i][j] == '1' else '0'
            self.maze.append(maze_tmp)
            self.marked.append(sub)

    def GetStart(self):
        for row in self.maze:
            for point in row:
                if point.val == 'S':
                    return point

    def GetEnd(self):
        for row in self.maze:
            for point in row:
                if point.val == 'E':
                    return point

    def IsMarked(self, point: Node):
        return self.marked[point.y][point.x] == '1'

    def ToMark(self, point: Node):
        if point.x == x_range - 1:
            self.marked[point.y] = self.marked[point.y][:-1] + '1'
        elif point.x == 0:
            self.marked[point.y] = '1' + self.marked[point.y][1:]
        else:
            self.marked[point.y] = self.marked[point.y][:point.x] + '1' + self.marked[point.y][point.x + 1:]

    def Include(self, next: list, queue: list):
        for node_expanded in next:
            for node in queue:
                if node_expanded == node:
                    self.m1 = node_expanded
                    return True
        return False

    def Neighbor(self, point: Node):
        neighbor = []
        global x_range, y_range

        if point.x + 1 < x_range and not self.IsMarked(self.maze[point.y][point.x + 1]):
            neighbor.append(self.maze[point.y][point.x + 1])
        if point.y + 1 < y_range and not self.IsMarked(self.maze[point.y + 1][point.x]):
            neighbor.append(self.maze[point.y + 1][point.x])
        if point.x - 1 >= 0 and not self.IsMarked(self.maze[point.y][point.x - 1]):
            neighbor.append(self.maze[point.y][point.x - 1])
        if point.y - 1 >= 0 and not self.IsMarked(self.maze[point.y - 1][point.x]):
            neighbor.append(self.maze[point.y - 1][point.x])
        return neighbor

    def Unidirectional_BFS(self):
        st, ed = self.GetStart(), self.GetEnd()
        queue = [st]
        while queue:
            n = len(queue)
            for k in range(n):
                temp = queue[0]
                temp_neighbor = self.Neighbor(temp)
                _path.append(temp)
                self.ToMark(temp)
                del queue[0]
                if temp == ed:
                    self.arrived = True
                    break
                else:
                    for point in temp_neighbor:
                        self.maze[point.y][point.x].par = [temp.x, temp.y]
                        queue.append(point)
            # queue完成一次刷新
            if self.arrived:
                break

    def Bidirectional_BFS(self):
        st, ed = self.GetStart(), self.GetEnd()
        qu_st, qu_ed = [st], [ed]
        while qu_ed and qu_st:
            nst = len(qu_st)
            ned = len(qu_ed)

            for k in range(nst):
                t1 = qu_st[0]
                t1_neighbor = self.Neighbor(t1)
                self.ToMark(t1)
                del qu_st[0]
                if self.Include(t1_neighbor, qu_ed):
                    self.m2 = t1
                    self.arrived = True
                    break
                else:
                    for point in t1_neighbor:
                        self.maze[point.y][point.x].par = [t1.x, t1.y]
                        qu_st.append(point)
            if self.arrived:
                break

            for k in range(ned):
                t2 = qu_ed[0]
                t2_neighbor = self.Neighbor(t2)
                self.ToMark(t2)
                del qu_ed[0]
                if self.Include(t2_neighbor, qu_st):
                    self.m2 = t2
                    self.arrived = True
                    break
                else:
                    for point in t2_neighbor:
                        self.maze[point.y][point.x].par = [t2.x, t2.y]
                        qu_ed.append(point)
            if self.arrived:
                break

    def UBFS_GetPath(self):
        p = []
        ed = self.GetEnd()
        while ed:
            p.append(self.maze[ed.y][ed.x])
            if ed.par:
                ed = self.maze[ed.par[1]][ed.par[0]]
            else:
                ed = None
        for point in p:
            # print(point)
            pass
        return p

    def BBFS_GetPath(self):
        # print('m1 = ', self.m1, 'm2 = ', self.m2)
        p = []
        while self.m1:
            p.append(self.maze[self.m1.y][self.m1.x])
            self.m1 = self.maze[self.m1.par[1]][self.m1.par[0]] if self.m1.par else None
        while self.m2:
            p.append(self.maze[self.m2.y][self.m2.x])
            self.m2 = self.maze[self.m2.par[1]][self.m2.par[0]] if self.m2.par else None
        for point in p:
            # print(point)
            pass
        return p
# end of class maze


def ReadData():
    global x_range, y_range
    file = open("MazeData.txt", 'r')
    content = file.read().split('\n')[:-1]
    file.close()

    x_range = len(content[0])
    y_range = len(content)
    print(x_range, y_range)
    for string in content:
        # print(' '.join(list(string)))
        pass
    return Maze(content)


def Show(path: list):
    answer = []
    for ii in range(y_range):
        answer.append(['·'] * x_range)
    for point in path:
        answer[point.y][point.x] = '@'
    for ii in answer:
        print(' '.join(ii))
    print('----------------')


if __name__ == '__main__':
    ubfs_maze = ReadData()
    bbfs_maze = copy.deepcopy(ubfs_maze)
    start = ubfs_maze.GetStart()
    end = ubfs_maze.GetEnd()
    print('start: ', start, '  end:', end)

    ubfs_start_time = time.perf_counter()
    ubfs_maze.Unidirectional_BFS()
    ubfs_end_time = time.perf_counter()
    print(ubfs_end_time - ubfs_start_time)

    bbfs_start_time = time.perf_counter()
    bbfs_maze.Bidirectional_BFS()
    bbfs_end_time = time.perf_counter()
    print(bbfs_end_time - bbfs_start_time)

    Show(_path)
    Show(ubfs_maze.UBFS_GetPath())
    print('This is Bidirectional_BFS: ')
    path = bbfs_maze.BBFS_GetPath()
    Show(path)
