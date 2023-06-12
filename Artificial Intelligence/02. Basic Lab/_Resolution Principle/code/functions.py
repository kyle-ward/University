from sources import *
import copy

# 两个functions.py的全局变量
# num记录着测试用例的子句个数，original_set记录着最原始的输入子句集
# （因为clause_set在后续的循环中会被不断添加新子句）
num = 0
original_set = []


# 需要外界输入的初始化函数
def Initial():
    clause_set = []
    # 引入全局变量
    global num, original_set
    num = int(input())
    for ii in range(num):
        # print(ii + 1 if ii > 8 else '0' + str(ii + 1), end='  ')
        clause_str = input()
        clause = Clause([])
        # 对输入的子句进行处理，子句内部原子公式数大于1时需要先去除最外面的括号
        clause_str = clause_str[1:-1] if clause_str[0] == '(' else clause_str
        literal = ''
        # 因为测试用例中的原子公式中会出现多个参数，故直接用split切分子句字符串，会导致原子公式也被切分（都是以', '作为分隔符）
        # 故此处采取依次遍历字符的方式，判断截取的标志为')'（但是当公式内部个体出现函数时会出现问题）
        for jj in range(len(clause_str)):
            literal += clause_str[jj]
            if clause_str[jj] == ')':
                # 需要的话去除掉前面的', '部分
                literal = literal[2:] if literal[0] == ',' else literal
                clause.literal_list.append(literal)
                literal = ''
        # 记录当前子句的索引，最后在整理输出格式的时候要用到
        clause.own = ii
        clause_set.append(clause)
    # 对original_set进行深拷贝，防止后续操作对其的影响
    original_set = copy.deepcopy(clause_set)
    return clause_set


# 此处的具体操作与Initial()函数大体一致
def DataProcessing(clause_set_str: list):
    clause_set = []
    global num, original_set
    num = len(clause_set_str)
    for ii in range(num):
        clause_str = clause_set_str[ii]
        clause = Clause([])
        clause_str = clause_str[1:-1] if clause_str[0] == '(' else clause_str
        literal = ''
        for jj in range(len(clause_str)):
            literal += clause_str[jj]
            if clause_str[jj] == ')':
                literal = literal[2:] if literal[0] == ',' else literal
                clause.literal_list.append(literal)
                literal = ''
        clause.own = ii
        clause_set.append(clause)
    original_set = copy.deepcopy(clause_set)
    return clause_set


# to/front
def Substitute(clause: Clause, substi: Substitution):
    for index in range(clause.length()):
        # 对于子句中的每个文字而言，只要有一个个体在替换的changelist中，就对该文字进行整体替换
        for individual in clause.getIndividualList(index):
            if individual in substi.from_list:
                tt = substi.from_list.index(individual)
                literal = clause.literal_list[index]
                # 对原子公式进行字符串替换（如果被替换对象在谓词中存在，会出现bug，故仅在谓词区域进行替换，最后再拼接回去）
                s1 = literal[literal.index('('):].replace(individual, substi.to_list[tt])

                clause.literal_list[index] = literal[:literal.index('(')] + s1
    return clause


# 判断两个子句能否被归结
# 为简化流程，这里将存在谓词互补作为进行归结的必要条件。而相同原子公式的消去则通过list(set())方式来解决
def AbleToGJ(clause1: Clause, clause2: Clause):
    for index1 in range(clause1.length()):
        for index2 in range(clause2.length()):
            # 二重循环遍历所有可能的谓词组合，如果不存在互补谓词，在二重循环结束之后返回false
            pred1, pred2 = clause1.getPredicate(index1), clause2.getPredicate(index2)
            if pred1 == Opposite(pred2):
                # 谓词符合条件，接下来比对谓词列表
                ind1_list, ind2_list = clause1.getIndividualList(index1), clause2.getIndividualList(index2)
                # 完全相同，直接赋值记录匹配谓词的索引，返回True
                if ind1_list == ind2_list:
                    clause1.mark_index, clause2.mark_index = index1, index2
                    return True
                # 以下都是必不完全相同的个体列表（一定会存在不匹配项）
                for ii in range(len(ind1_list)):
                    # 找到第一个不匹配项
                    if ind1_list[ii] != ind2_list[ii]:
                        # 此处为了简化流程，对于对应位置为不同变量的情形给予了false（有时间的话可以从此处着手优化）
                        # 两个都是常量，无法替换，直接返回false
                        if not IsVariable(ind1_list[ii]) and not IsVariable(ind2_list[ii]):
                            return False
                        # 一个常量一个变量，初步符合条件
                        if IsVariable(ind1_list[ii]) ^ IsVariable(ind2_list[ii]):
                            # 遍历其后续的个体组合，若相应位置上仍存在不同且都是常量的情况，返回false
                            for jj in range(ii + 1, len(ind1_list)):
                                if ind1_list[jj] != ind2_list[jj] and not IsVariable(ind1_list[jj]) and not IsVariable(ind2_list[jj]):
                                    return False
                            # 反之则认为符合归结条件，赋值记录匹配的公式索引，返回True
                            clause1.mark_index, clause2.mark_index = index1, index2
                            return True
    # 无互补谓词组合，返回false
    return False


# 最一般合一算法的初步实现
def MGU(ind1: list, ind2: list):
    # 初始化为空替换
    substi = Substitution([])
    # 当传入的两个个体列表已经相等时，不需要替换即可直接归结
    while ind1 != ind2:
        for ii in range(len(ind1)):
            # 在个体列表的对应位置找到第一个不匹配项，并确保其是一个变量一个常量
            # 在优化后的IsVariable函数中可以判断函数个体
            if ind1[ii] != ind2[ii] and IsVariable(ind1[ii]) ^ IsVariable(ind2[ii]):
                if IsVariable(ind1[ii]):
                    tt = [ind2[ii] + '/' + ind1[ii]]
                else:
                    tt = [ind1[ii] + '/' + ind2[ii]]
                # 依次对两个个体列表进行变量替换
                Substitution(tt).substitute(ind1)
                Substitution(tt).substitute(ind2)
                # 最后调用现成的复合函数
                substi.recombination(Substitution(tt))
                break
        # while end
    return substi


def GJ(clause1: Clause, clause2: Clause):
    # 初始化归结后子句的文字列表
    new_literal_list = []
    # 通过MGU生成最一般合一替换
    substi = MGU(clause1.getIndividualList(clause1.mark_index), clause2.getIndividualList(clause2.mark_index))
    # 对两个子句进行深拷贝，在进行替换合一，最后生成新子句并返回
    c1, c2 = copy.deepcopy(clause1), copy.deepcopy(clause2)
    c1, c2 = Substitute(c1, substi), Substitute(c2, substi)
    new_literal_list.extend(c1.literal_list)
    new_literal_list.extend(c2.literal_list)
    new_literal_list.remove(c1.literal_list[c1.mark_index])
    new_literal_list.remove(c2.literal_list[c2.mark_index])
    # 在最后进行一次set()调用，确保新子句集里面不会有相同的谓词
    return Clause(list(set(new_literal_list)), substi)


def Locate(clause: Clause, clause_set: list, helper: list):
    # 恢复其原来的father，mother值
    # 在前期的暴力循环中，每条子句被调用多次，father，mother值也被多次修改
    AbleToGJ(clause_set[clause.mother], clause_set[clause.father])
    # 初始化新索引
    mother_index, father_index = 0, 0
    for ii in range(len(helper)):
        if helper[ii].literal_list == clause_set[clause.father].literal_list:
            father_index = ii
        if helper[ii].literal_list == clause_set[clause.mother].literal_list:
            mother_index = ii

    # 进行一个规范化字符串赋值
    s1 = str(father_index + 1) + (chr(clause_set[clause.father].mark_index + 97) if clause_set[clause.father].length() > 1 else '')
    s2 = str(mother_index + 1) + (chr(clause_set[clause.mother].mark_index + 97) if clause_set[clause.mother].length() > 1 else '')
    s3 = []
    # 如果有替换的话进行替换的输出
    if clause.substi and clause.substi.change_list:
        for index in range(len(clause.substi.change_list)):
            s3.append(clause.substi.from_list[index] + '=' + clause.substi.to_list[index])
        return 'R[' + s1 + ',' + s2 + ']' + '(' + ', '.join(s3) + ')'
    else:
        return 'R[' + s1 + ',' + s2 + ']'


# 对总的子句集进行规范化输出的函数
def Regulate(clause_set: list):
    # 先采取BFS，将关键子句都筛选到simplify_set中
    root = 0
    simplify_set, queue = [], []
    for ii in range(len(clause_set)):
        if not clause_set[ii].literal_list:
            root = ii
            break
    queue.append(clause_set[root])
    while queue:
        n = len(queue)
        for ii in range(n):
            temp = queue[0]
            del queue[0]
            simplify_set.append(temp)
            if temp.mother >= num:
                queue.append(clause_set[temp.mother])
            if temp.father >= num:
                queue.append(clause_set[temp.father])

    # 得到了如下的simplify_set
    simplify_set.extend(original_set[::-1])
    for ii in range(len(simplify_set[::-1])):
        clause = simplify_set[::-1][ii]
        string = ', '.join(clause.literal_list) if clause.literal_list else '[]'
        # 为获得较好的观感：
        # 若采取DataProcessing进行初始化，则最好使用下面的四个print
        # 若采取Initial进行输入初始化，则最好只使用最后一个print
        if ii < num:
            print(ii + 1 if ii > 8 else '0' + str(ii + 1), end='  ')
            print('(' + string + ')' if clause.length() > 1 else string)
            pass
        else:
            print(ii + 1 if ii > 8 else '0' + str(ii + 1), end='  ')
            # 对精简过后的子句集的father，mother进行一个替换输出
            # (father, mother) 的值仍是在旧的全体子句集中的对应索引（不连贯且数值较大），现在要将其变为在简化子句集中的新索引
            print(Locate(clause, clause_set, simplify_set[::-1]) + ' = ' + string)


# 改进之后的初始化函数，可以处理原子公式内带函数括号的个体
def DataProcessing_opt(clause_set_str: list):
    clause_set = []
    global original_set, num
    for clause_str in clause_set_str:
        num = len(clause_set_str)
        clause = Clause([])
        clause_str = clause_str[1:-1] if clause_str[0] == '(' else clause_str
        stack1, stack2 = Stack(), Stack()
        literal = ''
        # ~A(f(x)), S(f(x)), C(f(x))
        # 设置两个栈来检测原子公式的末尾
        for ch in clause_str:
            literal += ch
            if ch == '(':
                stack1.push(ch)
                stack2.push(ch)
            if ch == ')':
                stack1.pop()
            if stack1.empty() and not stack2.empty():
                literal = literal[2:] if literal[0] == ',' else literal
                clause.literal_list.append(literal)
                stack2.clear()
                literal = ''
        clause_set.append(clause)
        original_set = copy.deepcopy(clause_set)
    return clause_set


