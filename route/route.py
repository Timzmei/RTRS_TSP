from coordinate.coordinates import calculate_distance


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
        length += calculate_distance(coordinates[route[i]], coordinates[route[i+1]])
    return length
