import math


def Locate(index):
    return index // 4, index % 4


def Manhattan_Distance(p1, p2):
    x1, y1 = Locate(p1)
    x2, y2 = Locate(p2)
    return abs(x1 - x2) + abs(y1 - y2)


def ManhattanSquare_Distance(p1, p2):
    return Manhattan_Distance(p1, p2) ** 2


def ManhattanOther_Distance(p1, p2):
    return Manhattan_Distance(p1, p2) ** 1.55


def Chebyshev_Distance(p1, p2):
    x1, y1 = Locate(p1)
    x2, y2 = Locate(p2)
    dx, dy = x1 - x2, y1 - y2
    return max(dx, dy)


def Euclidean_Distance(p1, p2):
    x1, y1 = Locate(p1)
    x2, y2 = Locate(p2)
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def Distance(p1, p2, _type):
    if _type == 'Manhattan':
        return Manhattan_Distance(p1, p2)
    elif _type == 'Manhattan Square':
        return ManhattanSquare_Distance(p1, p2)
    elif _type == 'Chebyshev':
        return Chebyshev_Distance(p1, p2)
    elif _type == 'Manhattan other':
        return ManhattanOther_Distance(p1, p2)
    elif _type == 'Euclidean':
        return Euclidean_Distance(p1, p2)


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


def CheckPoint_(_list: list, file):
    print('Checkpoint start')
    for index in range(4):
        for _state in _list:
            print(_state[4 * index:4 * index + 4], end='\t\t')
            file.write(_state[4 * index:4 * index + 4] + '\t\t')
        print()
        file.write('\n')
    print('steps:', len(_list) - 1)
    file.write('steps = ' + str(len(_list) - 1) + '\n')
    file.write('----------------------------------\n')
    print('checkpoint end')