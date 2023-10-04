from squares.square_class import Square
from route.route import calculate_nearest_point_to_center, find_nearest_point

def split_map_into_squares(coordinates):
    # Определяем максимальные и минимальные значения широты и долготы точек
    min_latitude = min(coordinates.values(), key=lambda x: x[0])[0]
    max_latitude = max(coordinates.values(), key=lambda x: x[0])[0]
    min_longitude = min(coordinates.values(), key=lambda x: x[1])[1]
    max_longitude = max(coordinates.values(), key=lambda x: x[1])[1]

    # Определяем размер квадрата по максимальным и минимальным координатам
    square_size_latitude = (max_latitude - min_latitude) / 2
    square_size_longitude = (max_longitude - min_longitude) / 2

    # Создаем словарь для хранения объектов Square с ключами - номерами квадратов
    squares = {}

    # Создаем квадраты и сохраняем их координаты и точки в каждом квадрате
    for i in range(2):
        for j in range(2):
            # Вычисляем координаты квадрата
            square_min_latitude = min_latitude + i * square_size_latitude
            square_max_latitude = min_latitude + (i + 1) * square_size_latitude
            square_min_longitude = min_longitude + j * square_size_longitude
            square_max_longitude = min_longitude + (j + 1) * square_size_longitude

            # Создаем объект Square и добавляем его в словарь с ключом - номером квадрата
            square = Square(i * 2 + j + 1, square_min_latitude, square_max_latitude, square_min_longitude, square_max_longitude)
            squares[square.number] = square

    # Находим точки, которые входят в каждый квадрат и обновляем объекты Square
    for point, coords in coordinates.items():
        lat, lon = coords
        for square in squares.values():
            if (square.min_latitude <= lat <= square.max_latitude) and (square.min_longitude <= lon <= square.max_longitude):
                square.add_point_inside(point)

    return squares


def update_square_points(square_route, coordinates):
    # Изначально начальная точка первого квадрата известна
    current_start_point = square_route.start_point
    squares = square_route.squares
    
    for index, square in enumerate(squares):
        # Вычисляем ближайшую точку к центру следующего квадрата
        if index < len(squares) - 1:
            next_square = squares[index + 1]
            end_point_inside = calculate_nearest_point_to_center(square.points_inside, next_square, coordinates)
            square.set_end_point_inside(end_point_inside)
        
        # Если это первый квадрат, то начальная точка уже установлена
        if index == 0:
            square.set_start_point_inside(1)
        else:
            # Иначе, вычисляем ближайшую точку к конечной точке предыдущего квадрата
            prev_square = squares[index - 1]
            points = square.points_inside.copy()
            # print(square.number)
            # print(points)
            # print(square.end_point_inside)
            if len(square.points_inside) > 1:
                points.remove(square.end_point_inside)
            start_point_inside = find_nearest_point(prev_square.end_point_inside, points, coordinates)
            if square.start_point_inside == None:
                square.set_start_point_inside(start_point_inside)
                
        if (len(square.points_inside) > 1 and square.start_point_inside == square.end_point_inside):
            points = square.points_inside.copy()
            points.remove(square.start_point_inside)
            end_point_inside = calculate_nearest_point_to_center(points, next_square, coordinates)
            square.set_end_point_inside(end_point_inside)


        # Обновляем текущую начальную точку для следующего квадрата
        current_start_point = square.end_point_inside

