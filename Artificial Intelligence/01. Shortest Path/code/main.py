import functions

solution = None
# 导入数据，生成城市列表并初始化无向图
graph = functions.GraphInit()
file = open("记录日志.txt", 'r+')
ll = file.read()
if len(file.read().split('\n')) >= 10:
    file.truncate(0)
file.write('--------------------------------\n->')

address, destination = input('请输入您的出发地与目的地：\n').split()
# 进行模糊匹配
address, destination = functions.CityMatch(address.title()), functions.CityMatch(destination.title())
if address == 'false' or destination == 'false':
    output = ('出发地' if address == 'false' else '目的地') + '输入错误，请再次检查'
    print(output)
    file.write(output + '\n')
else:
    solution = functions.Dijkstra(graph, address)
    distance = '最短距离为：' + str(solution.DistanceTo(destination)) + '\n'
    path = '最短路线为：' + ' -> '.join(solution.PathTo(destination)) + '\n          '
    check = '(' + solution.check + ' = ' + str(solution.DistanceTo(destination)) + ')'
    file.write(distance + '\n  ' + path + '\n')
    print('以下是查询结果：\n' + distance + path + check)

file.close()

