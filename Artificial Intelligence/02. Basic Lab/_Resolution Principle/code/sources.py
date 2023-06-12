test1 = ['GradStudent(sue)',
         '(~GradStudent(x), Student(x))',
         '(~Student(x), HardWorker(x))',
         '~HardWorker(sue)']
test2 = ['On(aa, bb)',
         'On(bb, cc)',
         'Green(aa)',
         '~Green(cc)',
         '(~On(x, y), ~Green(x), Green(y))']
test3 = ['A(tony)',
         'A(mike)',
         'A(john)',
         'L(tony, rain)',
         'L(tony, snow)',
         '(~A(x), S(x), C(x))',
         '(~C(y), ~L(y, rain))',
         '(L(z, snow), ~S(z))',
         '(~L(tony, u), ~L(mike, u))',
         '(L(tony, v), L(mike, v))',
         '(~A(w), ~C(w), S(w))']
# 将test3里面的部分变量变为了函数，使其变得更难处理了
test4 = ['A(tony)',
         'A(mike)',
         'A(john)',
         'L(tony, rain)',
         'L(tony, snow)',
         '(~A(f(x)), S(f(x)), C(f(x)))',
         '(~C(y), ~L(y, rain))',
         '(L(f(g(z)), snow), ~S(f(g(z))))',
         '(~L(tony, u), ~L(mike, u))',
         '(L(tony, v), L(mike, v))',
         '(~A(w), ~C(w), S(w))']
# DataProcessing函数的三个参数
# 如果需要用Initial()函数测试，文件最下面可直接复制三个测试用例


# 为方便实现MGU算法而设计的 替换 类
# changelist为记录所有变量替换的列表，采取和书中一样的 'to/from' 形式
# eg.['a/x', 'b/y']
# tolist为所有被替换后变量形成的列表，fromlist为所有需要被替换的变量列表
class Substitution:
    def __init__(self, change_list: list):
        self.change_list = change_list
        self.from_list, self.to_list = [], []
        for ss in change_list:
            self.to_list.append(ss[:ss.index('/')])
            self.from_list.append(ss[ss.index('/') + 1:])

    # 替换复合算法，函数参数为另一个Substitution变量
    def recombination(self, other_substitution):
        # 对self中所有变量进行替换迭代
        for ii in range(len(self.change_list)):
            for jj in range(len(other_substitution.change_list)):
                if self.to_list[ii] == other_substitution.from_list[jj]:
                    self.to_list[ii] = other_substitution.to_list[ii]
                    self.change_list[ii] = self.to_list[ii] + '/' + self.from_list[ii]

        # 将不在self.fromlist中的替换加入到self中来
        for ii in range(len(other_substitution.change_list)):
            if other_substitution.from_list[ii] not in self.from_list:
                self.change_list.append(other_substitution.change_list[ii])
                self.from_list.append(other_substitution.from_list[ii])
                self.to_list.append(other_substitution.to_list[ii])

        # 最后检查是否存在无效替换 eg. 'x/x'
        for ii in range(len(self.change_list)):
            if self.from_list[ii] == self.to_list[ii]:
                del self.from_list[ii]
                del self.to_list[ii]
                del self.change_list[ii]

    # 在MGU算法中进行的替换，被替换对象为原子公式的个体列表
    def substitute(self, individual_list: list):
        for index in range(len(individual_list)):
            if individual_list[index] in self.from_list:
                individual_list[index] = self.to_list[self.from_list.index(individual_list[index])]


# 子句类
# literal_list: 记录子句中的原子公式列表
# mark_index: 记录着子句中被（归结判断函数）所定位到的文字索引，方便归结函数后续快速定位到要被消除的公式位置
# mother, father, own: 记录着当前子句自己以及父母亲在子句集中的索引（如果是最开始的一组子句，父母一直都是默认值-1）
# substi: 记录得到当前子句时经过的替换，便于后续输出。原始子句的substi都是None类型
class Clause:
    def __init__(self, literal_list: list, substi = None):
        self.literal_list = literal_list
        self.substi = substi
        self.mark_index = 0
        self.mother = -1
        self.father = -1
        self.own = -1

    # 根据输入索引，返回相应位置原子公式的谓词
    def getPredicate(self, index):
        literal = self.literal_list[index]
        return literal[:literal.index('(')]

    # 根据输入索引，返回相应位置原子公式的个体列表（缺点：无法处理多变量函数作为个体变量（如果有的话））
    def getIndividualList(self, index):
        literal = self.literal_list[index]
        return literal[literal.index('(') + 1: -1].split(', ')

    # 返回子句的公式个数
    def length(self):
        return len(self.literal_list)


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, n):
        self.stack.append(n)

    def pop(self):
        del self.stack[-1]

    def top(self):
        return self.stack[-1]

    def empty(self):
        return self.stack == []

    def size(self):
        return len(self.stack)

    def clear(self):
        self.stack.clear()


# 将输入的谓词进行取反操作
def Opposite(predicate: str):
    if predicate[0] == '~':
        return predicate[1:]
    else:
        return '~' + predicate


# 对输入的个体，判断其是否是变量
def IsVariable(individual: str):
    while '(' in individual:
        individual = individual[individual.index('(') + 1: -1]
    return individual in ['x', 'y', 'z', 'u', 'v', 'w']


# 判断输入的子句集内是否含有空子句
def Has_NIL(clause_set: list):
    for clause in clause_set:
        if not clause.literal_list:
            return True
    return False


'''
test1:

4
GradStudent(sue)
(~GradStudent(x), Student(x))
(~Student(x), HardWorker(x))
~HardWorker(sue)


test2:

5
On(aa, bb)
On(bb, cc)
Green(aa)
~Green(cc)
(~On(x, y), ~Green(x), Green(y))


test3:

11
A(tony)
A(mike)
A(john)
L(tony, rain)
L(tony, snow)
(~A(x), S(x), C(x))
(~C(y), ~L(y, rain))
(L(z, snow), ~S(z))
(~L(tony, u), ~L(mike, u))
(L(tony, v), L(mike, v))
(~A(w), ~C(w), S(w))

'''