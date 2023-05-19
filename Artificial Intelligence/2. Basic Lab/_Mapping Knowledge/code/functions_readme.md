# functions.py 说明

> 主函数所调用的一些函数和辅助类的定义

```python
import math

mytest = ['Mother(James, Ann)',
          'Mother(James, Mike)',
          'Father(David, Mike)',
          'Couple(David, James)',
          'Sibling(Ann, Mike)']
test = ['Father(Jack, Dell)',
        'Father(Dell, Stephen)',
        'GrandFather(Jack, Stephen)',
        'Father(Dell, Seth)']
Variable_list = ['(x, y)', '(x, z)', '(y, x)', '(y, z)', '(z, x)', '(z, y)']
goal_knowledge = 'GrandFather(x, y)'
predicate_set = set()

# 判断是否是变量的基本函数
def IsVariable(ss: str):
    return ss in ['x', 'y', 'z']

# 边类，知识图谱的基本部分
class Edge:
    def __init__(self, pre, st, ed):
        self.predicate = pre
        self.st = st
        self.ed = ed

    # 判断两条边的顶点值是否匹配（都是不同的常量就要返回false）
    def ValueMatch(self, goal_after_change):
        if IsVariable(goal_after_change.st) and self.ed == goal_after_change.ed:
            return True
        elif IsVariable(goal_after_change.ed) and self.st == goal_after_change.st:
            return True
        elif self.st == goal_after_change.st and self.ed == goal_after_change.ed:
            return True
        elif IsVariable(goal_after_change.st) and IsVariable(goal_after_change.ed):
            return True
        else:
            return False

    # 打印函数，为打印类对象提供便利
    def Print(self):
        print(self.predicate + '(' + self.st + ', ' + self.ed + ')')


# 知识图谱类
class Graph:
    def __init__(self):
        self.edge_set = set()

    # 参数为规则，返回知识图谱中符合该规则的所有变量替换（是一个列表）
    # 此处简化了讨论，仅限于规则列表长度不大于二的情形
    def f1(self, rules: list):
        substitution = []
        # 只含有单个规则束缚
        if len(rules) == 1:
            rule = rules[0]
            for edge in self.edge_set:
                if edge.predicate == rule.predicate:
                    temp = {}
                    temp[rule.st] = edge.st
                    temp[rule.ed] = edge.ed
                    substitution.append(temp)
        # 含有两个规则束缚
        else:
            state = PredicateMatch(rules[0], rules[1])
            for e1 in self.edge_set:
                for e2 in self.edge_set:
                    if [rules[0].predicate, rules[1].predicate] == [e1.predicate, e2.predicate]:
                        temp = {}
                        if state == 'same' and [e1.st, e1.ed] == [e2.st, e2.ed]:
                            temp[rules[0].st], temp[rules[0].ed] = e1.st, e1.ed
                        elif state == 'reverse' and [e1.st, e1.ed] == [e2.ed, e2.st]:
                            temp[rules[0].st], temp[rules[0].ed] = e1.ed, e1.st
                        elif state == '00' and e1.st == e2.st:
                            temp[rules[0].st], temp[rules[0].ed], temp[rules[1].ed] = e1.st, e1.ed, e2.ed
                        elif state == '01' and e1.st == e2.ed:
                            temp[rules[0].st], temp[rules[0].ed], temp[rules[1].st] = e1.st, e1.ed, e2.st
                        elif state == '10' and e1.ed == e2.st:
                            temp[rules[0].st], temp[rules[0].ed], temp[rules[1].ed] = e1.st, e1.ed, e2.ed
                        elif state == '11' and e1.ed == e2.ed:
                            temp[rules[0].st], temp[rules[0].ed], temp[rules[1].st] = e1.st, e1.ed, e2.st
                        else:
                            pass
                        substitution.append(temp)
        return substitution


# 表格项类，代表了表格里面的每一行
class TableItem:
    def __init__(self, goal: Edge, rules: list, graph: Graph):
        self.graph = graph
        self.goal = goal
        self.pos, self.neg = 0, 0
        self.rules = rules
        self.value = 0
        # 对于表格的每一行的规则，通过调用graph的函数来计算对应的变量替换
        self.substitution = graph.f1(self.rules)
        for rule in rules:
            # print(changeToStr(rule), end=' ^ ')
            pass
        # print('\b\b      ', self.substitution)
        # 如果列表非空，则开始进行正反例的计算
        if self.substitution:
            self.CalcExample()

    # 根据替换对目标知识进行实例化
    def Instantiation(self):
        temp_list = []
        for item in self.substitution:
            if item:
                temp = Edge(self.goal.predicate, self.goal.st, self.goal.ed)

                for key in item.keys():
                    temp.st = item[key] if key == self.goal.st else temp.st
                    temp.ed = item[key] if key == self.goal.ed else temp.ed
                #temp.Print()
                # 此处转换为字符串是为了用set()进行去重
                temp_list.append(changeToStr(temp))
        return list(set(temp_list))

    def CalcExample(self):
        # 先依照替换，对目标知识进行变量替换（不改变其原始值）
        goals_after_change = self.Instantiation()
        #print('goals_after_change: ', goals_after_change, end='\n\n')
        # 对于目标知识每一种可能的实例化，对图谱的边集合进行遍历，计算符合条件的正反例数
        for goal_after_change in goals_after_change:
            #print(goal_after_change)
            goal_after_change = changeToEdge(goal_after_change)
            for edge in self.graph.edge_set:
                # 被计算进去的前提是，变量不能有冲突（例如对应位置有不同的常量）
                if edge.ValueMatch(goal_after_change):
                    # 若变量匹配但谓词不同，就是反例，反之就是正例
                    if edge.predicate == goal_after_change.predicate:
                        self.pos += 1
                    else:
                        self.neg += 1
                else:
                    continue

    # 表格项的便捷输出函数
    def Print(self):
        rules = []
        for rule in self.rules:
            rules.append(changeToStr(rule))
        rules_str = ' ^ '.join(rules)
        print(rules_str, '    ^m+ =', self.pos, '   ^m- =', self.neg, '    Gain:', self.value)

    # 计算增益值的函数
    def FOIL_Gain(self, pos, neg):
        if self.pos == 0:
            self.value = 'NA'
        else:
            self.value = str(round(self.pos * (math.log2(self.pos / (self.pos + self.neg)) - math.log2(pos / (pos + neg))), 2))

    # 状态函数，判断该项是否已经彻底推导出结论
    def State(self):
        return self.pos and not self.neg


# 进行表格打印，可以观察推理过程
def printTable(table: list):
    print('---------------------------')
    for item in table:
        item.Print()
    print('---------------------------')


# 判断是否已经得出正确的推导过程
def IsFinished(lst: list):
    for item in lst:
        if item.State():
            return True
    return False


# 进行边匹配（返回两个端点之间的关系，是完全相等，相反还是只有一个相等，并返回匹配索引）
def PredicateMatch(e1: Edge, e2: Edge):
    if [e1.st, e1.ed] == [e2.st, e2.ed]:
        return 'same'
    elif [e1.st, e1.ed] == [e2.ed, e2.st]:
        return 'reverse'
    else:
        if e1.st == e2.st:
            return '00'
        elif e1.st == e2.ed:
            return '01'
        elif e1.ed == e2.st:
            return '10'
        elif e1.ed == e2.ed:
            return '11'
        else:
            return 'false'


# Edge类和str的互化
def changeToEdge(pre: str):
    predicate = pre[:pre.index('(')]
    elements = pre[pre.index('(') + 1: -1].split(', ')
    return Edge(predicate, elements[0], elements[1])


def changeToStr(pre: Edge):
    return pre.predicate + '(' + pre.st + ', ' + pre.ed + ')'


# 初始化函数（含参不需输入）
def DataProc(test: list):
    mygraph = Graph()
    for knowledge in test:
        predicate = knowledge[:knowledge.index('(')]
        [st, ed] = knowledge[knowledge.index('(') + 1: -1].split(', ')
        predicate_set.add(predicate)
        mygraph.edge_set.add(Edge(predicate, st, ed))
    predicate_set.discard(goal_knowledge[:goal_knowledge.index('(')])

    print(len(test))
    for item in test:
        print(item)
    print()
    print(goal_knowledge, end='\n-------------------------------------\n')
    return mygraph

# 初始化函数（不含参需要输入）
def Initial():
    global goal_knowledge
    mygraph = Graph()
    num = int(input())
    for ii in range(num):
        knowledge = changeToEdge(input())
        mygraph.edge_set.add(knowledge)
        predicate_set.add(knowledge.predicate)
    goal_knowledge = input()
    predicate_set.discard(goal_knowledge[:goal_knowledge.index('(')])
    return mygraph


# 没任何前提得条件下计算正反例个数
def CreateExample(graph: Graph, goal: Edge):
    pos, neg = 0, 0
    for edge in graph.edge_set:
        if goal.predicate == edge.predicate:
            pos += 1
        else:
            neg += 1
    return pos, neg
```


