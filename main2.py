import math
import time
import multiprocessing


# Функция для вычисления расстояния между двумя точками на сфере (географические координаты)
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
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Расстояние между точками в километрах
    distance = radius * c
    return distance

# Функция для нахождения оптимального маршрута с использованием ближайшего соседа
def nearest_neighbor_partial(start, end, coordinates, result_queue, unvisited, lock):
    num_points = len(coordinates)
    current_point = start - 1
    route = [current_point]
    
    while unvisited:
        lock.acquire()  # Захватываем блокировку перед доступом к общим данным
        if current_point in unvisited:
            unvisited.remove(current_point)
        lock.release()  # Освобождаем блокировку после завершения операции

        nearest_point = min(unvisited, key=lambda point: calculate_distance(coordinates[current_point], coordinates[point - 1]))
        route.append(nearest_point - 1)
        current_point = nearest_point - 1

    result_queue.put(route)

    
def main():
    # Чтение координат из файла input.txt
    with open("input.txt", "r") as file:
        lines = file.readlines()
        coordinates = [tuple(map(float, line.strip().split(","))) for line in lines]

    # Измерение времени выполнения начинается здесь
    start_time = time.time()

    # Создание восеми рабочих потоков для расчетов
    num_threads = 8
    result_queue = multiprocessing.Queue()
    threads = []

    # Используем разделяемый список unvisited и блокировку
    manager = multiprocessing.Manager()
    unvisited = manager.list(range(len(coordinates)))
    lock = manager.Lock()

    chunk_size = len(coordinates) // num_threads

    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else len(coordinates) - 1
        thread = multiprocessing.Process(target=nearest_neighbor_partial, args=(start + 1, end + 1, coordinates, result_queue, unvisited, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Сбор и объединение результатов из очереди
    combined_route = []
    while not result_queue.empty():
        partial_route = result_queue.get()
        combined_route.extend(partial_route)

    # Вычисляем длину минимального маршрута
    min_distance = 0
    for i in range(len(combined_route) - 1):
        min_distance += calculate_distance(coordinates[combined_route[i]], coordinates[combined_route[i + 1]])

    # Измерение времени выполнения завершается здесь
    end_time = time.time()

    # Создание файла output.txt с результатами
    with open("output.txt", "w") as output_file:
        # Записываем фамилию, имя и отчество участника
        output_file.write("Иванов Иван Иванович\n")

        # Записываем длину минимального маршрута
        output_file.write(str(int(min_distance)) + "\n")

        # Записываем перестановку номеров объектов (как индексы в исходных данных)
        route_numbers = [str(index) for index in combined_route]
        output_file.write(",".join(route_numbers) + "\n")

    # Вычисляем время выполнения программы в секундах с десятичной дробью
    execution_time = end_time - start_time

    # Вывод сообщения об успешном завершении и времени выполнения
    print("Результаты сохранены в файл output.txt.")
    print(f"Время выполнения программы: {execution_time:.6f} секунд.")

if __name__ == '__main__':
    main()