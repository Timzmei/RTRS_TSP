from coordinates import calculate_distance
from square_route_class import SquareRoute

def build_square_route(squares_info, start_point, end_point):
    # Создаем объект маршрута обхода квадратов
    square_route = SquareRoute(start_point, end_point)
    
    # Определяем начальный квадрат
    current_square = None
    for square in squares_info.values():
        if start_point in square.points_inside:
            current_square = square
            square_route.add_square(current_square)
            break

    if current_square is None:
        raise ValueError("Начальная точка не найдена в квадратах.")

    # Определяем конечный квадрат
    end_square = None
    for square in squares_info.values():
        if end_point in square.points_inside:
            end_square = square
            break

    if end_square is None:
        raise ValueError("Конечная точка не найдена в квадратах.")

    # Исключаем квадраты без точек
    squares_with_points = [square for square in squares_info.values() if square != current_square and square != end_square and square.points_inside]

    # Пока есть квадраты с точками
    while squares_with_points:
        # Находим ближайший квадрат
        min_distance = float('inf')
        nearest_square = None

        for square in squares_with_points:
            distance = calculate_distance(current_square.calculate_center(), square.calculate_center())
            if distance < min_distance:
                min_distance = distance
                nearest_square = square

        # Если найден ближайший квадрат, добавляем его в маршрут
        if nearest_square:
            square_route.add_square(nearest_square)
            current_square = nearest_square
            squares_with_points.remove(nearest_square)
        else:
            break  # Выходим из цикла, если не осталось квадратов с точками

    # Добавляем конечный квадрат в конец маршрута для возврата
    square_route.add_square(end_square)

    return square_route


def build_route_inside_square(square, coordinates):
    
    # Получаем список точек внутри квадрата
    points_inside_square = square.points_inside.copy()
    
    # Создаем список для хранения маршрута внутри квадрата
    route_inside_square = [square.start_point_inside]

    if len(points_inside_square) > 1:
       
        # Исключаем начальную и конечную точки из списка точек внутри квадрата
        points_inside_square.remove(square.start_point_inside)
        if square.start_point_inside != square.end_point_inside:
            points_inside_square.remove(square.end_point_inside)

        while len(route_inside_square) <= len(points_inside_square):
            # Находим точку внутри квадрата, которая наиболее близка к текущей точке в маршруте
            closest_point = None
            min_distance = float('inf')
            current_point = route_inside_square[-1]

            for point in points_inside_square:
                if point not in route_inside_square:
                    distance = calculate_distance(coordinates[current_point], coordinates[point])
                    if distance < min_distance:
                        closest_point = point
                        min_distance = distance

            if closest_point is not None:
                route_inside_square.append(closest_point)
            else:
                break

        # Добавляем конечную точку в конец маршрута
        route_inside_square.append(square.end_point_inside)
        
    return route_inside_square


def build_full_route(square_route, coordinates):
    # Инициализируем список для хранения всего маршрута
    full_route = []

    # Добавляем начальную точку всего маршрута (точка с индексом 1)
    full_route.append(square_route.start_point)

    squares = square_route.squares.copy()
    
    if square_route.start_point == square_route.end_point:
        squares.pop()
        # for square in squares:
        #     print(square.points_inside)
    
    # Для каждого квадрата в маршруте обхода квадратов
    for square in squares:
        # Если это не первый квадрат, добавляем начальную точку внутри квадрата
        if len(full_route) > 1:
            full_route.append(square.start_point_inside)
        
        # Строим маршрут внутри квадрата и добавляем его к маршруту
        route_inside_square = build_route_inside_square(square, coordinates)
        full_route.extend(route_inside_square[1:])  # Исключаем повторение начальной точки

    # Добавляем конечную точку всего маршрута (точка с индексом 1)
    full_route.append(square_route.end_point)

    return full_route

def calculate_nearest_point_to_center(points_inside, next_square, coordinates):
    # Извлекаем координаты центра квадрата
    center_latitude = (next_square.min_latitude + next_square.max_latitude) / 2
    center_longitude = (next_square.min_longitude + next_square.max_longitude) / 2

    # Инициализируем переменные для хранения ближайшей точки и расстояния до нее
    nearest_point = None
    nearest_distance = float('inf')

    # Перебираем точки внутри квадрата и находим ближайшую к центру
    for point in points_inside:
        distance = calculate_distance(coordinates[point], (center_latitude, center_longitude))
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_point = point

    return nearest_point

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

def print_distance_route(coordinates, full_route):
    total_distance = calculate_route_length(full_route, coordinates)
    print(f"Длина всего маршрута: {total_distance} километров")
    
def calculate_route_length(route, coordinates):
    # Вычисляем общую длину маршрута на основе координат
    length = 0
    for i in range(len(route) - 1):
        length += calculate_distance(coordinates[route[i]], coordinates[route[i+1]])
    return length

def print_route_with_distances(route, coordinates):
    total_distance = 0
    route_with_distances = {}

    for i in range(len(route) - 1):
        current_point = route[i]
        next_point = route[i + 1]
        distance = calculate_distance(coordinates[current_point], coordinates[next_point])
        total_distance += distance
        route_with_distances[current_point] = distance

    # Добавляем последнюю точку маршрута без расстояния
    route_with_distances[route[-1]] = None

    print("Маршрут с расстояниями:")
    for point, distance in route_with_distances.items():
        if distance is not None:
            print(f"Точка {point}: {distance:.2f} километров до следующей точки")
        else:
            print(f"Точка {point}: конечная точка маршрута")
    
    print(f"Общая длина маршрута: {total_distance:.2f} километров")