import math
import numpy as np


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
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Расстояние между точками в километрах
    distance = radius * c
    return distance

def get_distance_mtrx(coordinates):
    distance_matrix = np.zeros((len(coordinates), len(coordinates)))
    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            if i != j:
                distance_matrix[i][j] = calculate_distance(coordinates[i + 1], coordinates[j + 1])
    return distance_matrix