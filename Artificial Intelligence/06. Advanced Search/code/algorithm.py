from tools import *
import math
import copy


# 局部搜索
class LocalSearch(Function):
    current_path = None  # 记录当前搜索路径
    record = Record()  # 记录搜索过程中的路径长度

    def __init__(self, _city_name, _city_location):
        super().__init__(_city_location, _city_name)  # 初始化基本数据
        self.max_times = 1000  # 最大循环次数（防止无限循环）

    # 在current_path的所有邻域解中，返回长度最短的那个
    def GenerateNewPath(self, current_path):
        shortest_path = []
        # 遍历cur_path所有可能的逆序组合，从中选择距离最短的一个最为后继
        for i in range(len(current_path)):
            for j in range(i + 1, len(current_path)):
                if i != j:
                    # 获取每一个可能的路径
                    temp = part_reverse(current_path, i, j)
                    if shortest_path:
                        shortest_path = temp if self.Evaluate(temp) < self.Evaluate(shortest_path) else shortest_path
                    else:
                        shortest_path = temp
        return shortest_path

    # 算法主体
    def Solve(self):
        cnt = 0
        self.current_path = self.initial_path
        print('init_path: ', self.initial_path)
        while cnt < self.max_times:
            print(cnt + 1, end=' ' if cnt % 40 != 39 else '\n')
            new_path = self.GenerateNewPath(self.current_path)
            if self.Evaluate(new_path) < self.Evaluate(self.current_path):
                self.current_path = new_path
            else:
                print('\n此时邻域中不存在更优的解了')
                print('循环结束，循环次数：', cnt + 1)
                return
            self.MakePathVisible(self.current_path)
            self.record.add_convergence_data(cnt + 1, self.Evaluate(self.current_path))
            cnt += 1
        print('\n循环结束，循环次数：', cnt)


# 可调参数：
# 1.初始温度：temperature
# 2.变化率：alpha
# 3.终止温度：final_temperature
# 4.邻域随温度扩展的剧烈程度：内循环次数可设为T的函数
class SimulateAnnealing(Function):
    current_path = None
    alpha = 0.99
    temperature = 400
    final_temperature = 0.08
    record = Record()
    best_path_of_cur_temperature = None

    def __init__(self, _city_name, _city_location):
        super().__init__(_city_location, _city_name)

    # 根据当前温度，在邻域内随机生成新解。温度越剧烈，新解与旧解之间的差距越大
    def GenerateNewPath(self, current_path):
        new_path = []
        # 当前温度越高，当前解内部的替换次数就越多
        for times in range(1):
            # 在范围内随机生成俩不等数
            while True:
                a = rd.randint(0, len(current_path) - 1)
                b = rd.randint(0, len(current_path) - 1)
                if a != b:
                    break
            new_path = part_reverse(self.current_path, min(a, b), max(a, b))
        return new_path

    # 算法主体
    def Solve(self):
        count = 0
        self.current_path = self.initial_path
        while self.temperature > self.final_temperature:
            print(count + 1, end=' ' if count % 60 != 59 else '\n')
            solution_list_of_cur_temperature = []
            f = self.Evaluate(self.current_path)
            # 在当前温度下随机生成多个（与温度相关）邻域解，循环完成之后到达当前温度的“平衡”
            for i in range(round(40 * len(self.city_location))):
                temp_path = self.GenerateNewPath(self.current_path)
                f_new = self.Evaluate(temp_path)
                if self.Metrospolis(f, f_new):
                    self.current_path = temp_path
                    solution_list_of_cur_temperature.append(temp_path)
            # 当前温度平衡时，从接受的解中选取最优的作为新的当前解，并降温
            if solution_list_of_cur_temperature:
                self.best_path_of_cur_temperature, min_distance = self.best(solution_list_of_cur_temperature)
                self.record.add_convergence_data(count + 1, min_distance)

            self.MakePathVisible(self.best_path_of_cur_temperature)
            self.temperature *= self.alpha
            # 计数
            count += 1
        # 退出循环，此时的current_path就是最优解

    def Metrospolis(self, f, f_new):  # Metropolis准则
        # 如果新解距离更短了，那么直接接受
        if f_new <= f:
            return 1
        # 不然，则有一定概率接受，概率如下
        else:
            p = math.exp((f - f_new) / self.temperature)
            if rd.random() < p:
                return 1
            else:
                return 0

    # 返回当前温度下接受的所有解中，距离最短的那个
    def best(self, solution_list):
        min_path, min_distance = None, float("inf")
        for index, solution in enumerate(solution_list):
            temp = self.Evaluate(solution)
            if temp < min_distance:
                min_distance = temp
                min_path = solution
        return min_path, min_distance


# 可调参数：
# 1.变异概率：mutate_probability
# 2.每代种群数目；num_per_generation
# 3.每一代繁殖后代的倍数（1倍即子女和父母同等数量）：n
# 4.繁殖迭代次数：generation_num
# 5.分组数量（应该是 num_per_generation 的因数之一）：group_num
class GeneticAlgorithm(Function):
    initial_path_list = []  # 初始种群（多点搜索待初始化变量）
    current_path_list = []  # 实时记录种群个体变化
    num_per_generation = 60  # 每代种群的个体数目
    generation_num = 2000  # 迭代/繁殖次数
    ls_times = 20  # 进行局部搜索的深度（用来进行初始值的优化）
    best_path = None
    record = Record()

    def __init__(self, _city_name, _city_location):
        super().__init__(_city_location, _city_name)
        self.n = 5  # 繁殖倍数（孩子个数：父母个数）
        self.city_num = len(_city_name)
        while True:
            temp_list = rand(1, self.city_num)
            if temp_list not in self.initial_path_list:
                self.initial_path_list.append(temp_list)
            if len(self.initial_path_list) == self.num_per_generation:
                break

        flag = 1  # 是否优化初始解
        if flag:
            for i in range(self.num_per_generation):
                print(i + 1, end=' ' if i % 20 != 19 else '\n')
                self.initial_path_list[i] = self.LocalSearch(self.initial_path_list[i])
            print('初始化结束')

    # 交叉 & 变异
    def CrossAndMutate(self):
        # 保持的部分为城市总数的三分之一
        keep_length = rd.randint(round(self.city_num * (2/5)), round(self.city_num * (3/5)))
        index_list = [i for i in range(self.city_num)]
        new_generation = []
        # 交叉部分
        # 此处每一代的种群数目最好是偶数个个体
        for i in range(0, len(self.current_path_list), 2):
            father_path = self.current_path_list[i]
            mother_path = self.current_path_list[i + 1]
            # 一对父母可以生成2 * n个孩子，n可以自定义
            for _ in range(self.n):
                son_path1 = ['0' for _ in range(self.city_num)]
                son_path2 = ['0' for _ in range(self.city_num)]
                father_a, mother_a = rd.choice(index_list[:-keep_length]), rd.choice(index_list[:-keep_length])
                father_b, mother_b = father_a + keep_length, mother_a + keep_length

                son1_choice_list = father_path[father_a: father_b]
                son2_choice_list = mother_path[mother_a: mother_b]
                son_path1[father_a: father_b] = son1_choice_list
                son_path2[mother_a: mother_b] = son2_choice_list

                son1_rest_index = index_list[:father_a] + index_list[father_b:]
                son2_rest_index = index_list[:mother_a] + index_list[mother_b:]
                # 填充son_path1
                for j in son1_rest_index:
                    for k in range(self.city_num):
                        if mother_path[k] not in son1_choice_list:
                            son_path1[j] = mother_path[k]
                            son1_choice_list.append(mother_path[k])
                            break
                # 填充son_path2
                for j in son2_rest_index:
                    for k in range(self.city_num):
                        if father_path[k] not in son2_choice_list:
                            son_path2[j] = father_path[k]
                            son2_choice_list.append(father_path[k])
                            break
                new_generation.extend([son_path1, son_path2])

        # 变异部分
        mutate_change = 0
        mutate_probability = 0.3
        for i in range(len(new_generation)):
            if rd.random() < mutate_probability:
                mutate_change += 1
                while True:
                    a, b = rd.choice(index_list), rd.choice(index_list)
                    if a != b:
                        break
                for j in range(rd.randint(1, 10)):
                    new_generation[i] = part_reverse(new_generation[i], min(a, b), max(a, b))
        self.current_path_list += new_generation

    # 锦标赛选择
    def Select(self, key=True):
        # 选择更加仿生的方式
        if key:
            # 应该满足：group_num * group_size = children_num + parent_num
            # win_num需要保证path_list长度不变
            group_num = 10  # 分几个组，设立时应该保证group_num可以被整除
            if self.num_per_generation % group_num:
                print('分组个数错误')
                return
            group_size = round(len(self.current_path_list) / group_num)  # 每组里有多少个个体
            win_num = round(self.num_per_generation / group_num)  # 每组里面可以被筛选出来的名额
            # 锦标赛胜出者列表
            winners = []
            for i in range(group_num):
                group = []
                for j in range(group_size):
                    temp = rd.choice(self.current_path_list)
                    group.append(temp)
                    self.current_path_list.remove(temp)
                group.sort(key=lambda x: self.Evaluate(x))
                winners += group[:win_num]
            # 一般此时需要保证 len(winners) == self.generation_num
            self.current_path_list = winners
        # 不仿生，直接从距离最短的个体开始选择
        else:
            self.current_path_list.sort(key=lambda x: self.Evaluate(x))
            self.current_path_list = self.current_path_list[:self.generation_num]

    # 算法主体
    def Solve(self):
        cur_best_path = []
        self.current_path_list = copy.deepcopy(self.initial_path_list)
        for i in range(self.generation_num):
            print(i + 1, end=' ' if i % 50 != 49 else '\n')
            self.CrossAndMutate()
            self.Select()
            cur_best_path = min(self.current_path_list, key=lambda x: self.Evaluate(x))
            cur_min_distance = self.Evaluate(cur_best_path)
            for path in self.current_path_list:
                if self.Evaluate(path) < cur_min_distance:
                    cur_best_path = path
                    cur_min_distance = self.Evaluate(path)
            self.record.add_convergence_data(i + 1, cur_min_distance)
            self.MakePathVisible(cur_best_path)

        self.best_path = cur_best_path

    # 对初始解集进行一系列的局部优化
    def LocalSearch(self, path):
        cnt = 0
        n = len(path)
        cur_path = copy.deepcopy(path)

        while cnt < self.ls_times:
            while True:
                a = rd.randint(0, n - 1)
                b = rd.randint(0, n - 1)
                if a != b:
                    break
            temp_path = part_reverse(cur_path, min(a, b), max(a, b))
            if self.Evaluate(temp_path) < self.Evaluate(cur_path):
                cur_path = temp_path
                cnt += 1
        return cur_path






























