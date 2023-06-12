import numpy as np
import matplotlib.pyplot as plt
import math
import random as rd


# 随机生成1 ~ n的组合序列
def rand(st: int, ed: int):
    result = [str(i) for i in range(st, ed + 1)]
    rd.shuffle(result)
    return result


# 列表的部分反转
def part_reverse(_list: list, a: int, b: int):
    result = []
    t1, t2, t3 = _list[:a], _list[a:b + 1], _list[b + 1:]
    result.extend(t1)
    t2.reverse()
    result.extend(t2)
    result.extend(t3)
    return result


class Visualization:
    # 绘制出退火距离收敛曲线，xs是外循环次数，ys是该次循环内的局部最短距离
    @staticmethod
    def draw_distance_convergence(xs_times, ys_min_distance):
        plt.plot(xs_times, ys_min_distance)
        plt.show()

    # 根据所有城市的坐标和路径列表，绘制算法运行期间的动态路径变化
    @staticmethod
    def RouteVisualization(city_location, route_list):
        pass


# 一些通用的变量以及基本函数
class Function(Visualization):
    city_location = None  # 城市坐标
    city_dict = None  # 城市名称：城市索引
    distance_matrix = None  # 城市距离矩阵
    initial_path = None  # 初始路径，限于单点搜索（局部搜索和模拟退火）

    def __init__(self, _city_location, _city_name):
        self.city_dict = dict(zip(_city_name, [i for i in range(len(_city_name))]))
        self.city_location = _city_location
        self.MatrixInit()
        self.PathInit('random')

    # 直接针对city_location生成matrix，与城市的具体名字无关
    def MatrixInit(self):
        self.distance_matrix = []
        # city1，city2都只代表索引
        for city1 in self.city_dict.keys():
            temp = []
            for city2 in self.city_dict.keys():
                a, b = self.city_dict[city1], self.city_dict[city2]
                distance = float("inf") if a == b else self.GetDistance(a, b)
                temp.append(distance)
            self.distance_matrix.append(temp)

    # 获取两个城市之间的距离
    def GetDistance(self, index1, index2):
        x1, y1 = self.city_location[index1]
        x2, y2 = self.city_location[index2]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # 路径初始化函数，可按编号生成或者随机生成
    def PathInit(self, init_type='random'):
        if init_type == 'random':
            self.initial_path = rand(1, len(self.city_location))
        elif init_type == 'simple':
            self.initial_path = [str(i + 1) for i in range(len(self.city_location))]
        elif init_type == 'particular':
            self.initial_path = [34, 53, 3, 19, 45, 79, 117, 1, 49, 70, 0, 40, 38,
                                 116, 111, 104, 61, 27, 114, 82, 29, 58, 89, 124, 84, 65,
                                 77, 120, 125, 113, 2, 107, 7, 17, 20, 32, 92, 36, 21, 39,
                                 46, 22, 95, 12, 66, 13, 9, 101, 5, 54, 121, 43, 41, 50, 59,
                                 119, 52, 105, 57, 48, 71, 90, 91, 72, 98, 73, 74, 51, 64, 55,
                                 8, 56, 81, 100, 122, 110, 118, 83, 35, 31, 112, 24, 47, 67, 97,
                                 109, 88, 93, 76, 102, 80, 11, 86, 37, 78, 94, 115, 23, 28, 14,
                                 99, 18, 26, 30, 16, 33, 42, 103, 126, 106, 62, 69, 96, 6, 25,
                                 87, 85, 68, 63, 123, 128, 60, 108, 75, 10, 4, 44, 15, 127]
            for i in range(len(self.initial_path)):
                self.initial_path[i] = str(self.initial_path[i] + 1)
            self.PrintPath(self.initial_path)
            print('特殊初始化结束')
        else:
            pass

    # 将路径城市点转换为边的集合
    def GetRoute(self, path):
        tour_route = []
        for i in range(len(path)):
            if i < len(path) - 1:
                a, b = self.city_dict[path[i]], self.city_dict[path[i + 1]]
                tour_route.append([a, b])
        return tour_route

    # 路径打印，以及输出相关信息
    def PrintPath(self, _path):
        path = _path + [_path[0]]
        answer = round(self.Evaluate(path[:-1]), 3)
        print('\npath: ', len(path))
        print(self.IsValidPath(_path))
        print(' -> '.join(path))
        basic = [6110, 2579][0]
        print('minimum distance:', answer, '\nerror：', round(((answer - basic) / basic) * 100, 3), '%')
        print('----------------------------------')

    # 返回某条路径的评估值，越小越好
    def Evaluate(self, _path):
        path = _path + [_path[0]]
        tour_route = self.GetRoute(path)
        total = 0.0
        for edge in tour_route:
            total += self.distance_matrix[edge[0]][edge[1]]
        return total

    # 判断当前路径是否是合法路径
    def IsValidPath(self, path):
        cmp = [str(i) for i in range(1, len(self.city_location) + 1)]
        for ch in path:
            if ch in cmp:
                cmp.remove(ch)
            else:
                return False
        if cmp:
            return False
        else:
            return True

    # 默认是对path进行动态绘图，如果输入其他字符串则转换为静态绘图
    def MakePathVisible(self, _path, key='active'):
        path = _path + [_path[0]]
        xs = np.array(self.city_location)[:, 0]
        ys = np.array(self.city_location)[:, 1]
        plt.clf()
        plt.scatter(xs, ys, s=8)
        tour_route = self.GetRoute(path)
        for edge in tour_route:
            p1 = self.city_location[edge[0]]
            p2 = self.city_location[edge[1]]
            _xs = np.array([p1[0], p2[0]])
            _ys = np.array([p1[1], p2[1]])
            plt.plot(_xs, _ys, 'b', linewidth=0.5)
        if key == 'active':
            plt.pause(0.0000001)
        else:
            plt.show()

    # 产生当前路径的后继路径
    def GenerateNewPath(self, current_path):
        return None


# 记录算法执行期间最优解的评估值，以及最后的图像打印输出
class Record:
    def __init__(self):
        self.convergence_data_xs = []
        self.convergence_data_ys = []

    def add_convergence_data(self, count: int, min_distance: float):
        self.convergence_data_xs.append(count)
        self.convergence_data_ys.append(min_distance)

    def Print(self):
        plt.clf()
        plt.plot(self.convergence_data_xs, self.convergence_data_ys, 'b')
        plt.show()





