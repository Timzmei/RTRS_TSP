import time

import random
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

    with open("input.txt", "r") as file:
        data = file.readlines()

    # Инициализируем словарь для хранения координат
    coordinates = {}

    # Перебираем строки файла и добавляем координаты в словарь
    for i, line in enumerate(data):
        # Разделяем строку на широту и долготу
        latitude, longitude = map(float, line.strip().split(','))
        # Сохраняем координаты в словарь, где ключ - номер точки, а значение - кортеж с координатами
        coordinates[i + 1] = (latitude, longitude)

    num_ants = 10
    num_iterations = 100
    pheromone_evaporation = 0.3
    pheromone_constant = 1.0
    alpha = 1.0
    beta = 2.0

    ant_route = ant_colony(coordinates, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha, beta)
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
    optimize_ant_route3 = optimize_route_2opt(optimize_ant_route2, coordinates, 1)
    optimize_ant_route4 = optimize_route_insert(optimize_ant_route3, coordinates, 5)
    optimize_ant_route5 = optimize_route_2opt(optimize_ant_route4, coordinates, 1)
    optimize_ant_route6 = optimize_route_insert(optimize_ant_route5, coordinates, 1)

    optimize_ant_route_length = calculate_route_length(optimize_ant_route, coordinates)
    optimize_ant_route_length1 = calculate_route_length(optimize_ant_route1, coordinates)
    optimize_ant_route_length2 = calculate_route_length(optimize_ant_route2, coordinates)
    optimize_ant_route_length3 = calculate_route_length(optimize_ant_route3, coordinates)
    optimize_ant_route_length4 = calculate_route_length(optimize_ant_route4, coordinates)
    optimize_ant_route_length5 = calculate_route_length(optimize_ant_route5, coordinates)
    optimize_ant_route_length6 = calculate_route_length(optimize_ant_route6, coordinates)
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
    print('Длина оптимизированного маршрута optimize_ant_route_length3:', optimize_ant_route_length3)
    # plot_map_earth(coordinates, optimize_ant_route3, optimize_ant_route_length3, 'optimize_ant_route3')
    print('Длина оптимизированного маршрута optimize_ant_route_length4:', optimize_ant_route_length4)
    # plot_map_earth(coordinates, optimize_ant_route4, optimize_ant_route_length4, 'optimize_ant_route4')
    print('Длина оптимизированного маршрута optimize_ant_route_length5:', optimize_ant_route_length5)
    # plot_map_earth(coordinates, optimize_ant_route5, optimize_ant_route_length5, 'optimize_ant_route5')
    print('Длина оптимизированного маршрута optimize_ant_route_length6:', optimize_ant_route_length6)
    plot_map_earth(coordinates, optimize_ant_route6, optimize_ant_route_length6, 'ant_route')

    # Создание файла output.txt с результатами
    with open("output.txt", "w") as output_file:
        # Записываем фамилию, имя и отчество участника
        output_file.write("Иванов Иван Иванович\n")

        # Записываем длину минимального маршрута
        output_file.write(str(int(optimize_ant_route_length1)) + "\n")

        # Записываем перестановку номеров объектов (как индексы в исходных данных)
        route_numbers = [str(index) for index in optimize_ant_route1]
        output_file.write(",".join(route_numbers) + "\n")


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
