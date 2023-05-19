from algorithm import *
import pandas as pd
import time


# 算法选择变量：1.局部搜索 2.模拟退火  3.遗传算法
# 其中生成初始值均使用随机生成（也可以在tools.py中改为固定初始值）
state = 2
if __name__ == '__main__':
    df = pd.read_csv('dataset/ch130.tsp', sep=' ', header=None, skiprows=6)
    city_name = np.array(df[0][0:len(df) - 1]).tolist()
    city_x, city_y = np.array(df[1][0:len(df) - 1]), np.array(df[2][0:len(df) - 1])
    city_location = list(zip(city_x, city_y))

    if state == 1:
        print('local search start:')
        local_search = LocalSearch(city_name, city_location)
        st = time.perf_counter()
        local_search.Solve()
        ed = time.perf_counter()
        print('local search costs', round(ed - st, 2), 'seconds')
        local_search.PrintPath(local_search.current_path)
        local_search.MakePathVisible(local_search.current_path, ' ')
        local_search.record.Print()
        print('local search end---------------------------------------------')
    elif state == 2:
        print('simulate annealing search start:')
        simulate_annealing = SimulateAnnealing(city_name, city_location)
        st = time.perf_counter()
        simulate_annealing.Solve()
        ed = time.perf_counter()
        print('\nsimulate annealing search costs', round(ed - st, 2), 'seconds')
        simulate_annealing.PrintPath(simulate_annealing.current_path)
        simulate_annealing.MakePathVisible(simulate_annealing.current_path, ' ')
        simulate_annealing.record.Print()
        print('simulate annealing search end--------------------------------')
    elif state == 3:
        print('genetic algorithm start:')
        genetic_algorithm = GeneticAlgorithm(city_name, city_location)
        st = time.perf_counter()
        genetic_algorithm.Solve()
        ed = time.perf_counter()
        print('\ngenetic algorithm costs', round(ed - st, 2), 'seconds')
        genetic_algorithm.PrintPath(genetic_algorithm.best_path)
        genetic_algorithm.MakePathVisible(genetic_algorithm.best_path, ' ')
        genetic_algorithm.record.Print()
    else:
        ga = GeneticAlgorithm(city_name, city_location)
        for path in ga.initial_path_list[:5]:
            ga.PrintPath(ga.LocalSearch(path))































