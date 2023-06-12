# 启发式搜索

<img src="file:///D:/《学习资料》/大二下/人工智能/[CS]%2021307261_wangjianyang/pictures/屏幕截图%202023-04-15%20141815.png" title="" alt="" width="412">

> main.py

启发式搜索程序入口

（需要自定义算法类别）

标志变量flag：为1选择A\*，为0选择IDA\*

```python
if flag:
    solution = A(example2, goal_state)
else:
    solution = IDA(example6, goal_state)
end_time = time.perf_counter()


if isinstance(solution, A):
    path = solution.GetPath()
    CheckPoint(path, file)
else:
    path = solution.GetPath()
    CheckPoint(path, file)
print(end_time - start_time)
```

> algorithm.py

定义了一些全局变量

算法类文件，存储状态类，A\*类和IDA\*类

（需要自定义启发函数类型）

CalcCost函数最后的`heuristic_functions_list`索引 -> 对应不同的启发函数类型

```python
heuristic_functions_list = ['Manhattan', 'Manhattan Square', 'Manhattan other', 'Chebyshev', 'Euclidean']


# State类的一部分
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
```

> functions.py

定义了各种启发函数，以及结果输出函数

曼哈顿指数为1,2,3时均有对应的启发函数，其他指数需要调用`Mangattanother_Distance`

（需要自定义`ManhattanOther_Distance`函数的返回值指数，文件里默认是1.55）

```python
def ManhattanOther_Distance(p1, p2):
    return Manhattan_Distance(p1, p2) ** 1.55
```

> output.txt

（由于实验报告截图不完整作出的一点优化）

记录输出结果具体路径，每次运行完代码之后可以在此查看具体过程

```python
def CheckPoint(_list: list, file):
    # print('Checkpoint start')
    for index in range(4):
        for _state in _list:
            print(_state.mat_str[4 * index:4 * index + 4], end='\t\t')
            file.write(_state.mat_str[4 * index:4 * index + 4] + '\t\t')
        print()
        file.write('\n')
    '''
    for _state in _list:
        print('gx=' + str(_state.gx), end='\t\t')
        file.write('gx = ' + str(_state.gx) + '\t\t')
    print()
    file.write('\n')
    for _state in _list:
        print('hx=' + str(round(_state.hx, 1)), end='\t\t')
        file.write('hx = ' + str(round(_state.hx, 2)) + '\t\t')
    '''
    print('steps =', len(_list) - 1)
    file.write('steps = ' + str(len(_list) - 1))
    # print('checkpoint end')
```
