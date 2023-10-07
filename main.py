import time
import random

from squares.squares import *
from route.route import *
from route.route_optimize import *
from map.map import *
from coordinate.coordinates import get_distance_mtrx


def main():
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

    with open("/home/timurg/PycharmProjects/RTRS_TSP/input3.txt", "r") as file:
        data = file.readlines()

    # Инициализируем словарь для хранения координат
    coordinates = {}

    # Перебираем строки файла и добавляем координаты в словарь
    for i, line in enumerate(data):
        # Разделяем строку на широту и долготу
        latitude, longitude = map(float, line.strip().split(','))
        # Сохраняем координаты в словарь, где ключ - номер точки, а значение - кортеж с координатами
        coordinates[i + 1] = (latitude, longitude)

    start_point = 1
    end_point = 1

    # squares = split_map_into_squares(coordinates)
    # route = build_square_route(squares, start_point, end_point)
    #
    # # Вызываем функцию для вычисления начальных и конечных точек внутри квадратов
    # update_square_points(route, coordinates)
    #
    # full_route = build_full_route(route, coordinates)
    # full_route_length = calculate_route_length(full_route, coordinates)
    #
    # # print("Полный маршрут:", full_route)
    # # print("Количество точек:", len(full_route))
    # print_distance_route(coordinates, full_route)
    #
    # optimized_route = optimize_route(coordinates, full_route)
    # # print_route_with_distances(optimized_route, coordinates)
    # route_length_2 = calculate_route_length(optimized_route, coordinates)
    # print("Количество точек:", len(optimized_route))
    # print("Длина оптимизированного маршрута:", route_length_2)
    #
    # # optimized_route_2 = optimize_route(coordinates, full_route)
    # # # print_route_with_distances(optimized_route, coordinates)
    # # optimized_route_length_2 = calculate_route_length(optimized_route_2, coordinates)
    # # print("Количество точек:", len(optimized_route_2))
    # # print("Длина оптимизированного маршрута другим манером:", optimized_route_length_2)
    #
    # optimize_route_3 = optimize_route_insert(optimized_route, coordinates, 1)
    # route_length_3 = calculate_route_length(optimize_route_3, coordinates)
    # # print("Полный маршрут:", optimize_route_3)
    # print("Количество точек:", len(optimize_route_3))
    # print("Длина оптимизированного маршрута:", route_length_3)
    #
    # # start_time = time.time()
    # optimize_route_4 = optimize_route_2opt(optimize_route_3, coordinates, 1)
    # route_length_4 = calculate_route_length(optimize_route_4, coordinates)
    # # # Записываем текущее время после выполнения кода
    # # end_time = time.time()
    #
    # # # Вычисляем время выполнения в секундах
    # # execution_time = end_time - start_time
    # # print(f"Время выполнения кода: {execution_time} секунд")
    #
    # # print("Полный маршрут:", optimize_route_4)
    # print("Количество точек:", len(optimize_route_4))
    # print(f"Длина оптимизированного маршрута optimize_route_4:", route_length_4)
    #
    # # Вызов функции для создания карты
    # plot_map_earth(coordinates, full_route, full_route_length, 'маршрут_full_route')
    # plot_map_earth(coordinates, optimized_route, route_length_2, 'маршрут_optimize_route')
    # # plot_map_earth(coordinates, optimized_route_2, optimized_route_length_2, 'маршрут_optimize_route_2')
    #
    # plot_map_earth(coordinates, optimize_route_3, route_length_3, 'маршрут_insert')
    # plot_map_earth(coordinates, optimize_route_4, route_length_4, 'маршрут_insert_2opt')

    # optimize_route_5 = optimize_route_insert(optimize_route_4, coordinates, 1)
    # route_length_5 = calculate_route_length(optimize_route_5, coordinates)
    # # print("Полный маршрут:", optimize_route_3)
    # print("Количество точек:", len(optimize_route_5))
    # print("Длина оптимизированного маршрута:", route_length_5)
    # plot_map_earth(coordinates, optimize_route_5, route_length_5, 'маршрут_optimize_2opt')

    # start_time = time.time()
    # optimize_route_6 = optimize_route_2opt_2(optimize_route_3, coordinates, 1)
    # route_length_6 = calculate_route_length(optimize_route_6, coordinates)
    # # Записываем текущее время после выполнения кода
    # end_time = time.time()

    # # Вычисляем время выполнения в секундах
    # execution_time = end_time - start_time
    # print(f"Время выполнения кода: {execution_time} секунд")

    # # print("Полный маршрут:", optimize_route_6)
    # print("Количество точек:", len(optimize_route_6))
    # print(f"Длина оптимизированного маршрута optimize_route_6:", route_length_6)
    # plot_map_earth(coordinates, optimize_route_6, route_length_6, 'маршрут_insert_optimize_2opt')

    num_ants = 10
    num_iterations = 150
    pheromone_evaporation = 0.3
    pheromone_constant = 1.5
    alpha = 1.0
    beta = 2.0
    best_pheromone_evaporation = 0.0
    best_pheromone_constant = 0.0
    best_num_ants = 0

    min_route_length1 = float('inf')

    # while pheromone_evaporation < 0.4:
    #
    #     pheromone_constant = 2.0
    #     while pheromone_constant < 3.6:
    #
    #         num_ants = 10
    #         while num_ants < 11:
    #             start_time1 = time.time()
    #
    #
    #             ant_route = ant_colony(coordinates, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha,
    #                                    beta)
    #             # print("Полный маршрут Ant:", ant_route)
    #             print("Количество точек маршрута Ant:", len(ant_route))
    #             ant_route_length = calculate_route_length(ant_route, coordinates)
    #             print(f'Длина маршрута Ant {pheromone_evaporation}, {pheromone_constant}, {num_ants}:', ant_route_length)
    #
    #             optimize_ant_route = optimize_route_insert(ant_route, coordinates, 3)
    #             optimize_ant_route1 = optimize_route_insert(ant_route, coordinates, 1)
    #
    #             optimize_ant_route_length = calculate_route_length(optimize_ant_route, coordinates)
    #             optimize_ant_route_length1 = calculate_route_length(optimize_ant_route1, coordinates)
    #
    #             # print("Полный маршрут optimize_ant_route_length:", optimize_ant_route)
    #             # print("Количество точек optimize_ant_route_length:", len(optimize_ant_route))
    #             print(f'Длина маршрута optimize_ant_route_length {pheromone_evaporation}, {pheromone_constant}, {num_ants}:', optimize_ant_route_length)
    #
    #             # print("Полный маршрут optimize_ant_route_length1:", optimize_ant_route1)
    #             # print("Количество точек optimize_ant_route_length1:", len(optimize_ant_route1))
    #             print(f'Длина маршрута optimize_ant_route_length1 {pheromone_evaporation}, {pheromone_constant}, {num_ants}:', optimize_ant_route_length1)
    #             print()
    #             print()
    #
    #             # Записываем текущее время после выполнения кода
    #             end_time1 = time.time()
    #
    #             # Вычисляем время выполнения в секундах
    #             execution_time1 = end_time1 - start_time1
    #             print(f"Время выполнения кода: {execution_time1} секунд")
    #
    #             if min_route_length1 > optimize_ant_route_length1:
    #                 min_route_length1 = optimize_ant_route_length1
    #                 best_pheromone_evaporation = pheromone_evaporation
    #                 best_pheromone_constant = pheromone_constant
    #                 best_num_ants = num_ants
    #             num_ants += 1
    #         pheromone_constant += 0.5
    #     pheromone_evaporation += 0.1
    #
    # print('min_route_length1 = ', min_route_length1, ', best_pheromone_evaporation = ', best_pheromone_evaporation, ', best_pheromone_constant = ', best_pheromone_constant, ', best_num_ants = ', best_num_ants)

    ant_route = ant_colony(coordinates, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha, beta)
    print("Полный маршрут Ant:", ant_route)
    print("Количество точек маршрута Ant:", len(ant_route))
    ant_route_length = calculate_route_length(ant_route, coordinates)
    print("Длина маршрута Ant:", ant_route_length)
    #
    plot_map_earth(coordinates, ant_route, ant_route_length, 'ant_route')
    #
    optimize_ant_route = optimize_route_insert(ant_route, coordinates, 1)
    optimize_ant_route1 = optimize_route_2opt(optimize_ant_route, coordinates, 1)

    optimize_ant_route_length = calculate_route_length(optimize_ant_route, coordinates)
    optimize_ant_route_length1 = calculate_route_length(optimize_ant_route1, coordinates)
    #
    # print("Полный маршрут optimize_ant_route_length:", optimize_ant_route)
    # print("Количество точек optimize_ant_route_length:", len(optimize_ant_route))
    print('Длина оптимизированного маршрута optimize_ant_route_length:', optimize_ant_route_length)
    plot_map_earth(coordinates, optimize_ant_route, optimize_ant_route_length, 'optimize_ant_route')
    #
    # print("Полный маршрут optimize_ant_route_length:", optimize_ant_route1)
    # print("Количество точек optimize_ant_route_length:", len(optimize_ant_route1))
    print('Длина оптимизированного маршрута optimize_ant_route_length:', optimize_ant_route_length1)
    plot_map_earth(coordinates, optimize_ant_route1, optimize_ant_route_length1, 'optimize_ant_route1')


def ant_colony(coordinates, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha, beta):
    distance_matrix = get_distance_mtrx(coordinates)
    optimized_route = ant_colony_optimization(distance_matrix, num_ants, num_iterations,
                                              pheromone_evaporation, pheromone_constant, alpha, beta)
    return optimized_route


if __name__ == '__main__':
    # Записываем текущее время перед выполнением кода
    start_time = time.time()

    main()

    # Записываем текущее время после выполнения кода
    end_time = time.time()

    # Вычисляем время выполнения в секундах
    execution_time = end_time - start_time
    print(f"Время выполнения кода: {execution_time} секунд")
