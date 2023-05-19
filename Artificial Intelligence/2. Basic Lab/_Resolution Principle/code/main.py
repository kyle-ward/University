from functions import *
# 主函数应该具备处理一下基本数据的能力：
# 1.子句集中每个子句含有多个文字（原子公式）
# 2.每个原子公式中不含有函数变量（原因是有的话会引入多个括号，变量替换需要另行分析

# 对于以下可能存在的情形，应尽量保证程序运行顺利
# 1.输入拼写错误或者子句集本来就无法证明
# 下面三个核心问题在于，无效左右括号以及逗号空格带来的干扰
# 2.子句集变量中含有多重嵌套函数时的子句切割
# 3.子句集中含有多元函数个体时候的子句切割


# 根据输入实现子句集的初始化，子句集为列表，子句为原子公式列表，每个原子公式以字符串形式存储
# clause_set = Initial()
# 懒得输入可以直接调用下面的函数，三个测试用例分别为test1，2，3
clause_set = DataProcessing_opt(test4)
# 开始处理，当子句集中开始存在空子句的时候停止循环，完成整个证明过程
while not Has_NIL(clause_set):
    # 每次采取暴力二重循环的方式进行归结
    lst = []
    i, cnt = 0, 0
    while i < len(clause_set):
        j = i + 1
        while j < len(clause_set):
            # 对于暴力枚举出来的每一个子句组合，先判断能否归结，在进行归结（防止出现太多的无用子句）
            if i != j and AbleToGJ(clause_set[i], clause_set[j]):
                new_clause = GJ(clause_set[i], clause_set[j])
                # 记录新子句是来自哪两个子句
                new_clause.father, new_clause.mother = i, j
                # 记录新子句本身在插入到子句集之后的索引
                new_clause.own = len(clause_set) + cnt
                cnt += 1
                # 对于归结出的新子句，如果立马加入到子句集中，会引起死循环（不知道为啥）
                # 故先将一轮二重循环的结果全部存储到临时子句集中，最后在一起压进子句集中
                lst.append(new_clause)
                pass
            j += 1
        i += 1
    # 一次二重遍历结束，将临时集压进子句集中
    clause_set.extend(lst)
    if len(clause_set) > 1000_0000:
        print('归结失败')
        break
# 对已经出现空子句的子句集进行规范化处理以及规范输出
if Has_NIL(clause_set):
    Regulate(clause_set)

