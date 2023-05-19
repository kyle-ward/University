from functions import *
import copy


# 10: a, 11: b, 12: c, 13: d, 14: e, 15: f
elements = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
example1 = ''.join('1248_57ba_df03_e69c'.split('_')) # 0.0150 ~ 0.3200
example2 = ''.join('5134_278c_96bf_0dae'.split('_')) # 0.0008 ~ 0.0075
example3 = ''.join('ea60_4918_235b_cd7f'.split('_'))
example4 = ''.join('6a3f_e87b_5102_dc94'.split('_'))
example5 = ''.join('b317_4682_f9ad_ec50'.split('_'))
example6 = ''.join('05fe_796d_12ca_8b43'.split('_'))

goal_state = ''.join('1234_5678_9abc_def0'.split('_'))
my_state = ''.join('5134_278c_96bf_dae0'.split('_'))
# 一些辅助变量，用以调整启发函数
heuristic_functions_list = ['Manhattan', 'Manhattan Square', 'Manhattan other', 'Chebyshev', 'Euclidean']


# 状态类，反映了某个状态需要的全部变量
class State:
    mat_str = None
    par_addr = None
    last_direction = None
    gx = None
    hx = None

    def __init__(self, cur: str, goal=''):
        self.mat_str = cur
        if goal != '':
            self.gx = 0
            self.CalcCost(goal)
            pass

    # 计算当前代价到终点的开销,可以选择启发函数
    def CalcCost(self, goal: str):
        self.hx = 0.0
        for i in range(len(elements)):
            temp1 = self.mat_str.index(elements[i])
            temp2 = goal.index(elements[i])
            # choose heuristic functions through its list
            self.hx += Distance(temp1, temp2, heuristic_functions_list[0])

    def fx(self):
        return self.gx + self.hx

    def __str__(self):
        return self.mat_str[:4] + '\n'  + self.mat_str[4:8] + '\n' + \
               self.mat_str[8:12] + '\n' + self.mat_str[12:16] + '\n' + \
               'gx = ' + str(self.gx) + '\t\thx = ' + str(self.hx) + '\n'

    # 方位移动函数，进行0的移动，并及时更新状态的父节点，gx以及hx值
    def up(self, goal: str):
        # index0 and index0 - 4 to change
        index0 = self.mat_str.index('0')
        # 可到达该点，且不走回头路
        if self.last_direction != 'down' and index0 > 3:
            # 0往上移动，target往下移动
            self.mat_str = self.mat_str[:index0 - 4] + self.mat_str[index0] + \
                           self.mat_str[index0 - 3:index0] + self.mat_str[index0 - 4] + \
                           self.mat_str[index0 + 1:]
            self.last_direction = 'up'
            self.gx += 1
            self.CalcCost(goal)
            return True
        else:
            return False

    def down(self, goal: str):
        index0 = self.mat_str.index('0')
        if self.last_direction != 'up' and index0 < 12:
            # 0往下移动，target往上移动
            self.mat_str = self.mat_str[:index0] + self.mat_str[index0 + 4] + \
                           self.mat_str[index0 + 1: index0 + 4] + self.mat_str[index0] + \
                           self.mat_str[index0 + 5:]
            self.last_direction = 'down'
            self.gx += 1
            self.CalcCost(goal)
            return True
        else:
            return False

    def left(self, goal: str):
        index0 = self.mat_str.index('0')
        if self.last_direction != 'right' and (index0 % 4) > 0:
            # 0往左移动，target往右移动
            self.mat_str = self.mat_str[:index0 - 1] + self.mat_str[index0] + \
                           self.mat_str[index0 - 1] + self.mat_str[index0 + 1:]
            self.last_direction = 'left'
            self.gx += 1
            self.CalcCost(goal)
            return True
        else:
            return False

    def right(self, goal: str):
        index0 = self.mat_str.index('0')
        if self.last_direction != 'left' and (index0 % 4) < 3:
            # 0往右移动，target往左移动
            self.mat_str = self.mat_str[:index0] + self.mat_str[index0 + 1] + \
                           self.mat_str[index0] + self.mat_str[index0 + 2:]
            self.last_direction = 'right'
            self.gx += 1
            self.CalcCost(goal)
            return True
        else:
            return False


# A*算法类
class A:
    open_list = []
    # close_list，一个存储状态，一个存储字符串，为的是适当用空间换时间
    close_list = []
    close_str_list = []
    start = None
    goal = None

    # 构造函数，同时也是算法的主体部分
    def __init__(self, start: str, goal: str):
        self.start = State(start, goal)
        self.goal = goal

        # start of A*
        self.open_list.append(self.start)
        while True:
            # 排序open_list，提取出fx最小的状态，并移至close_list
            self.open_list.sort(key=lambda x: (x.fx()), reverse=False)
            cur_state = self.open_list[0]
            del self.open_list[0]
            self.close_list.append(cur_state)
            self.close_str_list.append(cur_state.mat_str)

            # generate neighbor state
            ups = copy.deepcopy(cur_state)
            if ups.up(goal) and not self.InClose(ups.mat_str):
                ups.par_addr = self.close_list.index(cur_state)
                index = self.InOpen(ups.mat_str)
                # 如果已经在open中，则判断是否需要更新
                if index and self.open_list[index - 1].gx > ups.gx:
                    self.open_list[index - 1] = ups
                # 若不在open中，则加入open
                if not index:
                    self.open_list.append(ups)
                    # 每加入一个新元素，进行一个状态检查，遇到终点就退出循环（下面同理）
                    if ups.mat_str == goal:
                        print('Congratulations!')
                        break

            dns = copy.deepcopy(cur_state)
            if dns.down(goal) and not self.InClose(dns.mat_str):
                dns.par_addr = self.close_list.index(cur_state)
                index = self.InOpen(dns.mat_str)
                if index and self.open_list[index - 1].gx > dns.gx:
                    self.open_list[index - 1] = dns
                if not index:
                    self.open_list.append(dns)
                    if dns.mat_str == goal:
                        print('Congratulations!')
                        break

            lts = copy.deepcopy(cur_state)
            if lts.left(goal) and not self.InClose(lts.mat_str):
                lts.par_addr = self.close_list.index(cur_state)
                index = self.InOpen(lts.mat_str)
                if index and self.open_list[index - 1].gx > lts.gx:
                    self.open_list[index - 1] = lts
                if not index:
                    self.open_list.append(lts)
                    if lts.mat_str == goal:
                        print('Congratulations!')
                        break

            rts = copy.deepcopy(cur_state)
            if rts.right(goal) and not self.InClose(rts.mat_str):
                rts.par_addr = self.close_list.index(cur_state)
                index = self.InOpen(rts.mat_str)
                if index and self.open_list[index - 1].gx > rts.gx:
                    self.open_list[index - 1] = rts
                if not index:
                    self.open_list.append(rts)
                    if rts.mat_str == goal:
                        print('Congratulations!')
                        break

    # 判断是否在close中，直接用in可以提速五六倍
    def InClose(self, cur_state: str):
        return cur_state in self.close_str_list

    # 判断是否在open中，若在的话同时返回相应的索引信息（直接用index可能报错）
    def InOpen(self, cur_state: str):
        for index in range(len(self.open_list)):
            if self.open_list[index].mat_str == cur_state:
                return index + 1
        return 0

    # 返回路径
    def GetPath(self):
        print('path(A*) =')
        self.open_list.sort(key=lambda x: x.hx, reverse=False)
        path = []
        p = self.open_list[0]
        while p:
            path.append(p)
            if p.par_addr:
                p = self.close_list[p.par_addr]
            else:
                p = None
        path.append(self.start)
        return path[::-1]


# IDA*算法类
class IDA:
    goal_state = None
    visited = []
    visited_state = []
    state = False

    # 构造函数，也是算法主体
    def __init__(self, start: str, goal: str):
        self.start = State(start, goal)
        self.bound = self.max_cost = self.start.fx()
        self.goal = goal

        # 进行一次深度受限dfs，如果没有找到终点则更新bound继续搜索
        while True:
            self.min = 9999
            self.visited.clear()
            self.dfs(self.start)
            if self.state:
                break
            self.bound = self.min

    def dfs(self, cur_state: State):
        # 如果深度超出限制，则更新开销并返回
        if cur_state.fx() > self.bound:
            if self.min > cur_state.fx():
                self.min = cur_state.fx()
            return

        # visited记录所有被访问过的状态
        self.visited.append(cur_state.mat_str)
        self.visited_state.append(cur_state)
        if self.goal == cur_state.mat_str:
            self.goal_state = cur_state
            self.state = True
            return

        for state in self.neighbor(cur_state):
            if state.mat_str not in self.visited:
                self.dfs(state)
                if self.state:
                    return

    def neighbor(self, cur_state):
        neighbor = []
        ups = copy.deepcopy(cur_state)
        if ups.up(self.goal):
            ups.par_addr = self.visited_state.index(cur_state)
            neighbor.append(ups)
        dns = copy.deepcopy(cur_state)
        if dns.down(self.goal):
            dns.par_addr = self.visited_state.index(cur_state)
            neighbor.append(dns)
        lts = copy.deepcopy(cur_state)
        if lts.left(self.goal):
            lts.par_addr = self.visited_state.index(cur_state)
            neighbor.append(lts)
        rts = copy.deepcopy(cur_state)
        if rts.right(self.goal):
            rts.par_addr = self.visited_state.index(cur_state)
            neighbor.append(rts)
        # 排序以保证每次首次访问的都是fx最小的节点
        neighbor.sort(key=lambda x: x.fx(), reverse=False)
        return neighbor

    def GetPath(self):
        print('path(IDA*) = ')
        path = []
        p = self.goal_state
        while p:
            path.append(p)
            p = self.visited_state[p.par_addr] if p.par_addr else None
        path.append(self.start)
        return path[::-1]



