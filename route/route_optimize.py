import random
from multiprocessing import Pool
from functools import partial



from route.route import find_nearest_point, calculate_route_length

def optimize_route(coordinates, full_route):
    # Создаем список точек, которые нужно посетить (исключая начальную и конечную точки)
    points_to_visit = set(full_route[1:-1])  # Изменено для исключения первой и последней точек
    optimized_route = [full_route[0]]  # Начинаем с начальной точки

    current_point = full_route[0]

    while points_to_visit:
        nearest_point = find_nearest_point(current_point, points_to_visit, coordinates)
        optimized_route.append(nearest_point)
        points_to_visit.remove(nearest_point)
        current_point = nearest_point

    optimized_route.append(full_route[-1])  # Добавляем последнюю точку после завершения оптимизации
    
    # Возвращаем оптимизированный маршрут
    return optimized_route

def optimize_route_swap(route, coordinates):
    # Инициализируем переменные для хранения оптимального маршрута и его длины
    best_route = route.copy()
    best_length = calculate_route_length(route, coordinates)

    # Перебираем точки маршрута, кроме первой и последней
    for i in range(1, len(route) - 1):
        for j in range(i + 1, len(route) - 1):
            # Создаем копию маршрута для перестановки точек
            new_route = route.copy()
            # Переставляем точки i и j
            new_route[i], new_route[j] = new_route[j], new_route[i]
            
            # Вычисляем длину нового маршрута
            new_length = calculate_route_length(new_route, coordinates)

            # Если новая длина меньше лучшей, обновляем лучший маршрут и его длину
            if new_length < best_length:
                best_route = new_route
                best_length = new_length

    return best_route

# def optimize_route_insert(full_route, coordinates):
#     # Создаем копию маршрута для работы
#     optimized_route = full_route.copy()
    
#     # Инициализируем флаг, который будет показывать, была ли совершена хотя бы одна перестановка
#     improvement = True
    
#     while improvement:
#         improvement = False
#         for i in range(1, len(optimized_route) - 1):  # Не рассматриваем первую и последнюю точки
#             for j in range(1, len(optimized_route) - 1):  # Не рассматриваем первую и последнюю точки
#                 if i != j:
#                     # Создаем копию маршрута и вставляем точку i между точками j и j+1
#                     new_route = optimized_route.copy()
#                     point_to_insert = new_route.pop(i)
#                     new_route.insert(j, point_to_insert)
                    
#                     # Вычисляем длину нового маршрута
#                     new_length = calculate_route_length(new_route, coordinates)
                    
#                     # Вычисляем длину текущего маршрута
#                     current_length = calculate_route_length(optimized_route, coordinates)
                    
#                     # Если новый маршрут короче текущего, сохраняем его
#                     if new_length < current_length:
#                         optimized_route = new_route
#                         improvement = True
    
#     return optimized_route

def optimize_route_insert(full_route, coordinates, num_points_to_move):
    # Создаем копию маршрута для работы
    optimized_route = full_route.copy()
    
    # Инициализируем флаг, который будет показывать, была ли совершена хотя бы одна перестановка
    improvement = True
    
    while improvement:
        improvement = False
        for i in range(num_points_to_move, len(optimized_route) - num_points_to_move):  # Не рассматриваем первую и последнюю точки
            for j in range(num_points_to_move, len(optimized_route) - num_points_to_move):  # Не рассматриваем первую и последнюю точки
                if i != j:
                    # Создаем копию маршрута и перемещаем num_points_to_move точек начиная с i между точками j и j+1
                    new_route = optimized_route.copy()
                    points_to_move = new_route[i:i+num_points_to_move]
                    for point in points_to_move:
                        new_route.remove(point)
                    new_route[j:j] = points_to_move
                    
                    # Вычисляем длину нового маршрута
                    new_length = calculate_route_length(new_route, coordinates)
                    
                    # Вычисляем длину текущего маршрута
                    current_length = calculate_route_length(optimized_route, coordinates)
                    
                    # Если новый маршрут короче текущего, сохраняем его
                    if new_length < current_length:
                        optimized_route = new_route
                        improvement = True
    
    return optimized_route

# Функция для выполнения Муравьиного алгоритма в отдельном потоке
def run_colony(args, seed):
    distance_matrix, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha, beta = args
    random.seed(seed)  # Инициализация генератора случайных чисел с уникальным зерном
    # Остальной код вашей функции ant_colony_optimization()

    # Инициализация феромонов на ребрах
    num_points = len(distance_matrix)
    pheromone = [[1.0 for _ in range(num_points)] for _ in range(num_points)]

    global_ant_routes = []

    # Основной цикл Муравьиного алгоритма
    for iteration in range(num_iterations):
        ant_routes = []
        
        for ant in range(num_ants):
            current_point = random.randint(0, num_points - 1)
            unvisited_points = set(range(num_points)) - {current_point}
            ant_route = [current_point]
            
            while unvisited_points:
                # Вычисляем вероятности перехода в следующую точку
                probabilities = []
                for next_point in unvisited_points:
                    pheromone_value = pheromone[current_point][next_point]
                    distance_value = 1.0 / distance_matrix[current_point][next_point]
                    probability = (pheromone_value ** alpha) * (distance_value ** beta)
                    probabilities.append((next_point, probability))
                
                # Выбираем следующую точку на основе вероятностей
                total_probability = sum(probability for (_, probability) in probabilities)
                choice = random.uniform(0, total_probability)
                cumulative_probability = 0
                for (next_point, probability) in probabilities:
                    cumulative_probability += probability
                    if cumulative_probability >= choice:
                        break
                
                # Переходим в выбранную точку и обновляем маршрут
                current_point = next_point
                unvisited_points.remove(current_point)
                ant_route.append(current_point)
            
            ant_routes.append(ant_route)
        
        # Обновляем феромоны на ребрах
        pheromone = [[pheromone[i][j] * (1 - pheromone_evaporation) for j in range(num_points)] for i in range(num_points)]
        for ant_route in ant_routes:
            route_length = sum(distance_matrix[i][j] for i, j in zip(ant_route, ant_route[1:]))
            for i, j in zip(ant_route, ant_route[1:]):
                pheromone[i][j] += pheromone_constant / route_length
        
        # Находим лучший маршрут на текущей итерации
        best_route = min(ant_routes, key=lambda route: sum(distance_matrix[i][j] for i, j in zip(route, route[1:])))
        best_route_length = sum(distance_matrix[i][j] for i, j in zip(best_route, best_route[1:]))

        
        # Выводим лучший маршрут на текущей итерации
        # print(f"Iteration {iteration + 1}: Best Route = {best_route}, Length = {best_route_length}")
        global_ant_routes.append((best_route, best_route_length))


    return global_ant_routes


def ant_colony_optimization(distance_matrix, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha, beta):
    
    num_colonies = 4  # Количество колоний муравьев
    
    with Pool(num_colonies) as pool:
        seeds = range(num_colonies)
        # Создайте частичную функцию с фиксированными аргументами, которые вы хотите передать
        partial_run_colony = partial(run_colony, (distance_matrix, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha, beta))
        # Теперь используйте partial_run_colony в pool.map()
        global_ant_routes = pool.map(partial_run_colony, seeds)
        
        # print(len(global_ant_routes))
    
        min_length = float('inf')
        best_route = None

        for data in global_ant_routes:
            for route, length in data:
              
                # print(route)
                # print(length)
            
                if length < min_length:
                    min_length = length
                    best_route = route


        print(best_route)
        print(min_length)
            

        # На выходе получим лучший найденный маршрут
        # print(f"Best Route: {global_best_route}, Length: {global_bst_route_length}")
        
        # Найдем индекс числа 1 в списке
        route = list(best_route)
        
        ant_route = [x+1 for x in route]
        indx = ant_route.index(1)

        # Создаем новый список с левой частью от 1 в конце
        new_ant_route = ant_route[indx:] + ant_route[:indx]
        new_ant_route.append(1)
    
    return new_ant_route