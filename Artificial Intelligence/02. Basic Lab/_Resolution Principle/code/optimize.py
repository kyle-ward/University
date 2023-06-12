from sources import Clause, Stack
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


# 对输入的个体，判断其是否是变量
def IsVariable(individual: str):
    while '(' in individual:
        individual = individual[individual.index('(') + 1: -1]
    return individual in ['x', 'y', 'z', 'u', 'v', 'w']


def DataProcessing_opt(clause_set_str: list):
    clause_set = []
    for clause_str in clause_set_str:
        clause = Clause([])
        clause_str = clause_str[1:-1] if clause_str[0] == '(' else clause_str
        stack1, stack2 = Stack(), Stack()
        literal = ''
        # ~A(f(x)), S(f(x)), C(f(x))
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
    return clause_set


clause_set = DataProcessing_opt(test4)
for clause in clause_set:
    print(clause.literal_list)

print('-----------------------')
ss = 'f(x)'
if IsVariable(ss):
    print(ss)











