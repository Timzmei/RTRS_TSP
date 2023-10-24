import time
import os
# import logging
import sys
from multiprocessing import freeze_support

from route.route_optimize import *
from coordinate.coordinates import get_distance_mtrx






def begin():
    # Записываем текущее время перед выполнением кода
    start_time = time.time()
    # input("Начало цикла main...")



    # Получите путь к текущей директории (где находится ваш exe файл)
    # exe_directory = os.path.dirname(sys.executable)
    # exe_directory = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        # Скрипт запущен как экзешник (скомпилированный)
        exe_directory = os.path.dirname(sys.executable)
    else:
        # Скрипт запущен из исходного кода (из IDE)
        exe_directory = os.path.dirname(os.path.abspath(__file__))
    # Затем используйте относительные пути относительно текущей директории
    file_path_input = os.path.join(exe_directory, "input.txt")
    file_path_output = os.path.join(exe_directory, "output.txt")

    coordinates = read_file({}, file_path_input)

    num_ants = 10
    num_iterations = 100
    pheromone_evaporation = 0.3
    pheromone_constant = 1.0
    alpha = 1.0
    beta = 2.0


    ant_route = ant_colony(coordinates, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha,
                           beta)

    optimize_ant_route = optimize_route_insert(ant_route, coordinates, 1)
    optimize_ant_route1 = optimize_route_2opt(optimize_ant_route, coordinates, 1)
    optimize_ant_route2 = optimize_route_insert(optimize_ant_route1, coordinates, 1)

    optimize_ant_route_length2 = calculate_route_length(optimize_ant_route2, coordinates)

    # Записываем текущее время после выполнения кода
    end_time = time.time()

    # Вычисляем время выполнения в секундах
    execution_time = end_time - start_time
    # print(f"Время выполнения кода: {execution_time} секунд")

    # Создание файла output.txt с результатами
    write_file(file_path_output, optimize_ant_route2, optimize_ant_route_length2, execution_time)


def write_file(file_path_output, optimize_ant_route2, optimize_ant_route_length2, execution_time):
    with open(file_path_output, "w") as output_file:
        # Записываем фамилию, имя и отчество участника
        output_file.write("Гулиев Тимур Абрекович\n")
        # output_file.write(f"Время выполнения: {execution_time}\n")
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
    optimized_route = ant_colony_optimization(distance_matrix, num_ants, num_iterations,
                                              pheromone_evaporation, pheromone_constant, alpha, beta)
    return optimized_route

if __name__ == '__main__':

    # Записываем текущее время перед выполнением кода
    start_time = time.time()
    # input("Начало цикла main...")
    if sys.platform == "win32":
        freeze_support()
    begin()

    # Записываем текущее время после выполнения кода
    end_time = time.time()

    # Вычисляем время выполнения в секундах
    execution_time = end_time - start_time
    # print(f"Время выполнения кода: {execution_time} секунд")
    # input("Начало цикла main...")
