dit = {1: 1, 2: 2, 3: 3}

try:
    print(dit[1])
except NameError:
    print('Name wrong!')
except KeyError:
    print('Key wrong!')
else:
    print('else!')
finally:
    print('finally!')

try:
    print(dit[4])
except NameError:
    print('Name wrong!')
except KeyError:
    print('Key wrong!')
else:
    print('else!')
finally:
    print('finally!')