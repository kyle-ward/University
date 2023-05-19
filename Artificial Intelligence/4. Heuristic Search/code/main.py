from algorithm import *
import time


file = open("output.txt", 'w')
start_time = time.perf_counter()
flag = 1
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













