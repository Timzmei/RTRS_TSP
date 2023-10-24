import time
import os
import sys
import random
from collections import deque
from multiprocessing import Pool
from functools import partial
import math



def main():
    # Получите путь к текущей директории (где находится ваш exe файл)
    exe_directory = os.path.dirname(sys.executable)
    # exe_directory = os.path.dirname(os.path.abspath(__file__))
    # Затем используйте относительные пути относительно текущей директории
    file_path_input = os.path.join(exe_directory, "input.txt")
    file_path_output = os.path.join(exe_directory, "output.txt")

    print(exe_directory)
    print(file_path_input)
    # Инициализируем словарь для хранения координат
    coordinates = {}
    # # Генерируем 100 уникальных координат
    # unique_coordinates = set()
    # while len(unique_coordinates) < 100:
    #     lat = round(random.uniform(-90, -66), 6)  # Широта [-66, -90]
    #     lon = round(random.uniform(-180, 180), 6)  # Долгота [-180, 180]
    #     unique_coordinates.add((lat, lon))

    # # Записываем координаты в файл input.txt
    # with open("input2.txt", "w") as file:
    #     for coord in unique_coordinates:
    #         lat, lon = coord
    #         file.write(f"{lat},{lon}\n")

    # print("Файл input.txt успешно создан с 100 уникальными координатами.")
    coordinates = read_file(coordinates, file_path_input)

    num_ants = 10
    num_iterations = 100
    pheromone_evaporation = 0.3
    pheromone_constant = 1.0
    alpha = 1.0
    beta = 2.0

    keys = list(coordinates.keys())
    print("Количество точек маршрута coordinates:", len(keys))
    input("Нажмите Enter для завершения coordinates...")
    # keys_length = calculate_route_length(keys, coordinates)
    # print("Длина маршрута coordinates:", keys_length)
    # ant_route = [1, 26, 54, 67, 23, 43, 48, 97, 91, 37, 28, 15, 45, 74, 86, 46, 96, 88, 35, 19, 27, 89, 39, 10, 7, 41, 85, 36, 77, 16, 21, 13, 82, 78, 98, 25, 8, 83, 52, 53, 64, 4, 90, 72, 65, 49, 51, 92, 80, 79, 60, 44, 69, 30, 17, 11, 66, 50, 56, 100, 55, 20, 18, 94, 76, 42, 12, 71, 33, 40, 31, 84, 59, 75, 47, 63, 68, 24, 62, 87, 9, 70, 34, 38, 3, 95, 61, 14, 22, 57, 5, 32, 99, 29, 6, 93, 81, 2, 73, 58, 1]
    ant_route = ant_colony(coordinates, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha,
                           beta)
    input("Нажмите Enter для завершения ant_route...")

    print("Полный маршрут Ant:", ant_route)
    print("Количество точек маршрута Ant:", len(ant_route))
    ant_route_length = calculate_route_length(ant_route, coordinates)
    print("Длина маршрута Ant:", ant_route_length)
    #
    # plot_map_earth(coordinates, ant_route, ant_route_length, 'ant_route')
    #
    optimize_ant_route = optimize_route_insert(ant_route, coordinates, 1)
    optimize_ant_route1 = optimize_route_2opt(optimize_ant_route, coordinates, 1)
    optimize_ant_route2 = optimize_route_insert(optimize_ant_route1, coordinates, 1)
    # optimize_ant_route3 = optimize_route_2opt(optimize_ant_route2, coordinates, 1)
    # optimize_ant_route4 = optimize_route_insert(optimize_ant_route3, coordinates, 5)
    # optimize_ant_route5 = optimize_route_2opt(optimize_ant_route4, coordinates, 1)
    # optimize_ant_route6 = optimize_route_insert(optimize_ant_route5, coordinates, 1)

    optimize_ant_route_length = calculate_route_length(optimize_ant_route, coordinates)
    optimize_ant_route_length1 = calculate_route_length(optimize_ant_route1, coordinates)
    optimize_ant_route_length2 = calculate_route_length(optimize_ant_route2, coordinates)
    # optimize_ant_route_length3 = calculate_route_length(optimize_ant_route3, coordinates)
    # optimize_ant_route_length4 = calculate_route_length(optimize_ant_route4, coordinates)
    # optimize_ant_route_length5 = calculate_route_length(optimize_ant_route5, coordinates)
    # optimize_ant_route_length6 = calculate_route_length(optimize_ant_route6, coordinates)
    #
    # print("Полный маршрут optimize_ant_route_length:", optimize_ant_route)
    # print("Количество точек optimize_ant_route_length:", len(optimize_ant_route))
    print('Длина оптимизированного маршрута optimize_ant_route_length:', optimize_ant_route_length)
    # plot_map_earth(coordinates, optimize_ant_route, optimize_ant_route_length, 'optimize_ant_route')
    #
    # print("Полный маршрут optimize_ant_route_length:", optimize_ant_route1)
    # print("Количество точек optimize_ant_route_length:", len(optimize_ant_route1))
    print('Длина оптимизированного маршрута optimize_ant_route_length1:', optimize_ant_route_length1)
    # plot_map_earth(coordinates, optimize_ant_route1, optimize_ant_route_length1, 'optimize_ant_route1')
    print('Длина оптимизированного маршрута optimize_ant_route_length2:', optimize_ant_route_length2)
    # plot_map_earth(coordinates, optimize_ant_route2, optimize_ant_route_length2, 'optimize_ant_route2')
    # print('Длина оптимизированного маршрута optimize_ant_route_length3:', optimize_ant_route_length3)
    # # plot_map_earth(coordinates, optimize_ant_route3, optimize_ant_route_length3, 'optimize_ant_route3')
    # print('Длина оптимизированного маршрута optimize_ant_route_length4:', optimize_ant_route_length4)
    # # plot_map_earth(coordinates, optimize_ant_route4, optimize_ant_route_length4, 'optimize_ant_route4')
    # print('Длина оптимизированного маршрута optimize_ant_route_length5:', optimize_ant_route_length5)
    # # plot_map_earth(coordinates, optimize_ant_route5, optimize_ant_route_length5, 'optimize_ant_route5')
    # print('Длина оптимизированного маршрута optimize_ant_route_length6:', optimize_ant_route_length6)
    # plot_map_earth(coordinates, optimize_ant_route2, optimize_ant_route_length2, 'ant_route')

    # Создание файла output.txt с результатами
    write_file(file_path_output, optimize_ant_route2, optimize_ant_route_length2)


def write_file(file_path_output, optimize_ant_route2, optimize_ant_route_length2):
    with open(file_path_output, "w") as output_file:
        # Записываем фамилию, имя и отчество участника
        output_file.write("Гулиев Тимур Абрекович\n")

        # Записываем длину минимального маршрута
        output_file.write(str(int(optimize_ant_route_length2)) + "\n")

        # Записываем перестановку номеров объектов (как индексы в исходных данных)
        route_numbers = [str(index) for index in optimize_ant_route2]
        output_file.write(",".join(route_numbers) + "\n")


def read_file(coordinates, file_path_input):
    try:
        with open(file_path_input, 'r') as file:
            data = file.readlines()

        # Перебираем строки файла и добавляем координаты в словарь
        for i, line in enumerate(data):
            # Разделяем строку на широту и долготу
            latitude, longitude = map(float, line.strip().split(','))
            # Сохраняем координаты в словарь, где ключ - номер точки, а значение - кортеж с координатами
            coordinates[i + 1] = (latitude, longitude)
    except FileNotFoundError:
        print("Файл не найден. Убедитесь, что путь к файлу указан правильно.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
    return coordinates


def ant_colony(coordinates, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha, beta):
    distance_matrix = get_distance_mtrx(coordinates)
    input("Нажмите Enter для завершения ant_colony...")

    optimized_route = ant_colony_optimization(distance_matrix, num_ants, num_iterations,
                                              pheromone_evaporation, pheromone_constant, alpha, beta)
    return optimized_route


def optimize_route_2(coordinates, full_route):
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


def optimize_route_insert(full_route, coordinates, num_points_to_move):
    # Создаем копию маршрута в виде списка
    optimized_route = list(full_route)

    # Инициализируем флаг, который будет показывать, была ли совершена хотя бы одна перестановка
    improvement = True

    while improvement:
        improvement = False
        i = num_points_to_move
        while i < len(optimized_route) - num_points_to_move:
            j = num_points_to_move
            while j < len(optimized_route) - num_points_to_move:
                if i != j:
                    # Создаем копию маршрута и перемещаем num_points_to_move точек начиная с i между точками j и j+1
                    new_route = list(optimized_route)
                    points_to_move = new_route[i:i + num_points_to_move]
                    for _ in range(num_points_to_move):
                        new_route.pop(i)
                    for point in reversed(points_to_move):
                        new_route.insert(j, point)

                    # Вычисляем длину нового маршрута
                    new_length = calculate_route_length(new_route, coordinates)

                    # Вычисляем длину текущего маршрута
                    current_length = calculate_route_length(optimized_route, coordinates)

                    # Если новый маршрут короче текущего, сохраняем его
                    if new_length < current_length:
                        optimized_route = new_route
                        improvement = True
                j += 1
            i += 1

    return optimized_route


def optimize_route_2opt_2(full_route, coordinates, num_points_to_move):
    # Создаем копию маршрута для работы
    optimized_route = full_route.copy()

    # Вычисляем длину текущего маршрута
    current_length = calculate_route_length(optimized_route, coordinates)

    # Инициализируем флаг, который будет показывать, была ли совершена хотя бы одна перестановка
    improvement = True

    while improvement:
        improvement = False
        for i in range(num_points_to_move,
                       len(optimized_route) - num_points_to_move):  # Не рассматриваем первую и последнюю точки
            for j in range(i + 1,
                           len(optimized_route) - num_points_to_move):  # Не рассматриваем первую и последнюю точки
                if i != j:
                    # Создаем копию маршрута и переворачиваем подпоследовательность между i и j
                    new_route = optimized_route.copy()
                    new_route[i:j + 1] = reversed(new_route[i:j + 1])

                    # Вычисляем длину нового маршрута
                    new_length = calculate_route_length(new_route, coordinates)

                    # Если новый маршрут короче текущего, сохраняем его
                    if new_length < current_length:
                        optimized_route = new_route
                        current_length = new_length
                        improvement = True

    return optimized_route


def optimize_route_2opt(full_route, coordinates, num_points_to_move):
    # Создаем копию маршрута для работы
    optimized_route = full_route.copy()

    # Вычисляем длину текущего маршрута
    current_length = calculate_route_length(optimized_route, coordinates)

    # Инициализируем флаг, который будет показывать, была ли совершена хотя бы одна перестановка
    improvement = True

    while improvement:
        improvement = False
        for i in range(num_points_to_move, len(optimized_route) - num_points_to_move):
            for j in range(i + 1, len(optimized_route) - num_points_to_move):
                if i != j:
                    # Создаем копию маршрута и переворачиваем подпоследовательность между i и j
                    new_route = optimized_route[i:j + 1][::-1]
                    new_route = optimized_route[:i] + new_route + optimized_route[j + 1:]

                    # Вычисляем длину нового маршрута
                    new_length = calculate_route_length(new_route, coordinates)

                    # Если новый маршрут короче текущего, сохраняем его
                    if new_length < current_length:
                        optimized_route = new_route
                        current_length = new_length
                        improvement = True

    return optimized_route


def run_colony(args, seed):
    distance_matrix, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha, beta = args
    random.seed(seed)  # Инициализация генератора случайных чисел с уникальным зерном

    num_points = len(distance_matrix)
    pheromone = [[1.0 for _ in range(num_points)] for _ in range(num_points)]

    global_ant_routes = []

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
        pheromone = [[pheromone[i][j] * (1 - pheromone_evaporation) for j in range(num_points)] for i in
                     range(num_points)]
        for ant_route in ant_routes:
            route_length = sum(distance_matrix[i][j] for i, j in zip(ant_route, ant_route[1:]))
            for i, j in zip(ant_route, ant_route[1:]):
                pheromone[i][j] += pheromone_constant / route_length

        # Находим лучший маршрут на текущей итерации
        best_route = min(ant_routes, key=lambda route: sum(distance_matrix[i][j] for i, j in zip(route, route[1:])))
        best_route_length = sum(distance_matrix[i][j] for i, j in zip(best_route, best_route[1:]))

        global_ant_routes.append((best_route, best_route_length))

    return global_ant_routes


# Остальной код функции ant_colony_optimization

def ant_colony_optimization(distance_matrix, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha,
                            beta):
    input("Нажмите Enter для продолжения  ant_colony_optimization...")

    num_colonies = 6  # Количество колоний муравьев

    with Pool(num_colonies) as pool:
        seeds = range(num_colonies)
        # print('seeds = ', seeds)
        # Создайте частичную функцию с фиксированными аргументами
        partial_run_colony = partial(run_colony, (
            distance_matrix, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha, beta))
        # Теперь используйте partial_run_colony в pool.map()
        global_ant_routes = pool.map(partial_run_colony, seeds)

    min_length = float('inf')
    best_route = None

    for data in global_ant_routes:
        for route, length in data:
            if length < min_length:
                min_length = length
                best_route = route

    route = list(best_route)
    ant_route = [x + 1 for x in route]
    indx = ant_route.index(1)
    new_ant_route = ant_route[indx:] + ant_route[:indx]
    new_ant_route.append(1)

    return new_ant_route

# Функция для вычисления расстояния между двумя точками по координатам
def calculate_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Радиус Земли в километрах (приближенное значение)
    radius = 6371.0

    # Переводим градусы в радианы
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Разница между долготами и широтами
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Формула гаверсинуса для расчета расстояния
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Расстояние между точками в километрах
    distance = radius * c
    return distance


def get_distance_mtrx(coordinates):
    num_points = len(coordinates)
    distance_matrix = [[0.0] * num_points for _ in range(num_points)]

    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                distance_matrix[i][j] = calculate_distance(coordinates[i + 1], coordinates[j + 1])

    return distance_matrix


def find_nearest_point(point, point_list, coordinates):
    nearest_point = None
    nearest_distance = float('inf')

    for other_point in point_list:
        if other_point != point:
            distance = calculate_distance(coordinates[point], coordinates[other_point])
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_point = other_point

    return nearest_point


def calculate_route_length(route, coordinates):
    # Вычисляем общую длину маршрута на основе координат
    length = 0
    for i in range(len(route) - 1):
        length += calculate_distance(coordinates[route[i]], coordinates[route[i + 1]])
    return length


if __name__ == '__main__':
    # Записываем текущее время перед выполнением кода
    start_time = time.time()
    input("Начало цикла main...")
    main()

    # Записываем текущее время после выполнения кода
    end_time = time.time()

    # Вычисляем время выполнения в секундах
    execution_time = end_time - start_time
    print(f"Время выполнения кода: {execution_time} секунд")
