import random
import math
import numpy as np
from functools import partial
from multiprocessing import Pool
from deap import base, creator, tools, algorithms

# Шаг 1: Определение пространства параметров
# Диапазоны значений параметров
param_ranges = {
    "alpha": (0, 5),
    "beta": (0, 5),
    "num_ants": (2, 100),
    "num_iterations": (10, 1000),
}

# Шаг 2: Определение целевой функции
# Ваша функция для оценки длины маршрута должна быть определена здесь

# Создаем класс для минимизации (цель - минимизировать длину маршрута)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", dict, fitness=creator.FitnessMin)

min_pheromone_evaporation = 0.01
max_pheromone_evaporation = 0.5
min_pheromone_constant = 1.0
max_pheromone_constant = 5.0

def calculate_route_length(route, coordinates):
    # Вычисляем общую длину маршрута на основе координат
    length = 0
    for i in range(len(route) - 1):
        length += calculate_distance(coordinates[route[i] - 1], coordinates[route[i + 1] - 1])

    return length

# Функция для вычисления матрицы расстояний
def get_distance_mtrx(coordinates):
    distance_matrix = np.zeros((len(coordinates), len(coordinates)))
    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            if i != j:
                distance_matrix[i][j] = calculate_distance(coordinates[i + 1], coordinates[j + 1])
    return distance_matrix


# Функция для вычисления расстояния между координатами
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

# Шаг 3: Создание начальной популяции
def create_individual():
    # Генерируем случайные значения для параметров
    params = {
        "alpha": random.uniform(param_ranges["alpha"][0], param_ranges["alpha"][1]),
        "beta": random.uniform(param_ranges["beta"][0], param_ranges["beta"][1]),
        "num_ants": random.randint(param_ranges["num_ants"][0], param_ranges["num_ants"][1]),
        "num_iterations": random.randint(param_ranges["num_iterations"][0], param_ranges["num_iterations"][1]),
        "pheromone_evaporation": random.uniform(min_pheromone_evaporation, max_pheromone_evaporation),
        "pheromone_constant": random.uniform(min_pheromone_constant, max_pheromone_constant)
    }
    return params

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.5, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Шаг 4: Генетический алгоритм
def evaluate_individual(individual):
    # Извлекаем параметры из individual
    alpha = individual["alpha"]
    beta = individual["beta"]
    num_ants = int(individual["num_ants"])  # Преобразуем в целое число
    num_iterations = int(individual["num_iterations"])  # Преобразуем в целое число
    pheromone_evaporation = individual["pheromone_evaporation"]
    pheromone_constant = individual["pheromone_constant"]

    # Создаем distance_matrix
    distance_matrix = get_distance_mtrx(coordinates)

    # Здесь вызываем вашу функцию муравьиного алгоритма и передаем параметры
    ant_routes = run_ant_colony_optimization(
        (distance_matrix, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha, beta))

    # Находим лучший маршрут и его длину

    # best_route = min(ant_routes, key=lambda route: sum(distance_matrix[i][j] for i, j in zip(route, route[1:])))
    # best_route_length = sum(distance_matrix[i][j] for i, j in zip(best_route, best_route[1:]))

    best_route_length = float('inf')  # Инициализируем длину лучшего маршрута как бесконечность
    best_route = None  # Инициализируем лучший маршрут как пустой

    # Перебираем все маршруты и находим наименьший
    for route, route_length in ant_routes:
        # Если найденный маршрут короче текущего лучшего, обновляем лучший маршрут
        if route_length < best_route_length:
            best_route_length = route_length
            best_route = route

    # В best_route теперь хранится лучший маршрут

    # Возвращаем сумму длин лучших маршрутов в виде кортежа
    return (best_route_length,)
# Замените эту функцию на вашу реализацию муравьиного алгоритма
def run_ant_colony_optimization(params):
    distance_matrix, num_ants, num_iterations, pheromone_evaporation, pheromone_constant, alpha, beta = params
    random.seed(42)  # Инициализация генератора случайных чисел с уникальным зерном

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
                    distance_value = 1.0 / distance_matrix[current_point - 1][next_point - 1]
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

toolbox.register("evaluate", evaluate_individual)

# Шаг 5: Оптимизация параметров муравьиного алгоритма с помощью генетического алгоритма
def optimize_ant_colony_parameters():
    population_size = 50
    num_generations = 10

    # Создание начальной популяции
    population = toolbox.population(n=population_size)

    # Генерация статистики
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("min", min)

    # Запуск генетического алгоритма
    algorithms.eaMuPlusLambda(population, toolbox, mu=population_size, lambda_=population_size * 2, cxpb=0.7, mutpb=0.2, ngen=num_generations, stats=stats, halloffame=None, verbose=True)

    # Получение лучших параметров
    best_individual = tools.selBest(population, k=1)[0]
    best_parameters = best_individual.items()
    best_fitness = best_individual.fitness.values[0]

    # Вывод найденных оптимальных параметров
    print("Лучшие параметры:")
    for param, value in best_parameters:
        print(f"{param}: {value}")

if __name__ == "__main__":
    # Запуск оптимизации параметров муравьиного алгоритма
    with open("/home/timurg/PycharmProjects/RTRS_TSP/input2.txt", "r") as file:
        data = file.readlines()

    # Инициализируем словарь для хранения координат
    coordinates = {}

    # Перебираем строки файла и добавляем координаты в словарь
    for i, line in enumerate(data):
        # Разделяем строку на широту и долготу
        latitude, longitude = map(float, line.strip().split(','))
        # Сохраняем координаты в словарь, где ключ - номер точки, а значение - кортеж с координатами
        coordinates[i + 1] = (latitude, longitude)
    optimize_ant_colony_parameters()