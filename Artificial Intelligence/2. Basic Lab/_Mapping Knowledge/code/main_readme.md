# main.py 说明

> 知识图谱算法主函数

（两个graph初始化函数可以选择调用）

```python
from functions import *
'''
5
Mother(James, Ann)
Mother(James, Mike)
Father(David, Mike)
Couple(David, James)
Sibling(Ann, Mike)

Father(x, y)
'''

# 根据测试用例初始化知识图谱，直接运行即可(但是需要修改functions.py里面的goal_knowledge)
graph = DataProc(test)
# graph = Initial()

# 在整个图谱上搜索正反例个数
pos, neg = CreateExample(graph, changeToEdge(goal_knowledge))
rules_append, table, changes = [], [], []

# 一次while循环即为目标知识推导出一个前提知识
while not IsFinished(table):
    table.clear()
    # 按照每一行来依次构建表格，并在表格项构造函数中就计算好各项数值
    for predicate in predicate_set:
        for xy in Variable_list:
            rules = [changeToEdge(predicate + xy)]
            rules.extend(rules_append)
            temp = TableItem(changeToEdge(goal_knowledge), rules, graph)
            # 计算每一项的增益值
            temp.FOIL_Gain(pos, neg)
            table.append(temp)
    # printTable(table)

    # 找出表格里面的最大增益值，并加入到新规则列表中
    index, max_value = -1, -1.0
    for item in table:
        if item.value != 'NA' and float(item.value) > max_value:
            max_value, index = float(item.value), table.index(item)
    rules_append = table[index].rules
    # 记录对应的变量替换，便于后期查找所有符合目标谓词的知识组合
    changes = table[index].substitution
    # 更新全局的正反例数值
    pos, neg = table[index].pos, table[index].neg
    for rule in rules_append:
        # rule.Print()
        pass
    # print('----------------------while ended-----------------------------')

file = open("result.txt", 'r+')

inferences, conclusion = [], []
# 一些规范化输出代码
for rule in rules_append:
    conclusion.append(changeToStr(rule))
print('(' + ' ^ '.join(conclusion) + ') -> ' + goal_knowledge)
# print(changes)

for change in changes:
    mark = 1
    tt = changeToEdge(goal_knowledge)
    if change:
        tt.st, tt.ed = change[tt.st], change[tt.ed]
        # 每一个替换都对应着一个实例，剔除掉原先就属于知识图谱的实例之后（例如本来就存在的Father(David, Mike)），再依次输出
        for edge in graph.edge_set:
            if changeToStr(tt) == changeToStr(edge):
                mark -= 1
        if mark:
            inferences.append(changeToStr(tt))
for inference in inferences:
    print(inference)
```
