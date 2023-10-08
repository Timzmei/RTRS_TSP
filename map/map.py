import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def choose_projection(coordinates):
    # Определите минимальные и максимальные значения широты и долготы на основе координат маршрута.
    min_lat = min(latitude for latitude, _ in coordinates.values())
    max_lat = max(latitude for latitude, _ in coordinates.values())
    min_lon = min(longitude for _, longitude in coordinates.values())
    max_lon = max(longitude for _, longitude in coordinates.values())

    # Проверьте, находится ли маршрут в области полюсов.
    is_polar_region = min_lat <= -60 or max_lat >= 60

    # Определите проекцию в зависимости от области мира.
    if is_polar_region:
        # Для области полюсов используйте проекцию spstere с настройками boundinglat и lon_0.
        return {'projection': 'spstere', 'boundinglat': -60, 'lon_0': (min_lon + max_lon) / 2}
    else:
        # Для остальных случаев, используйте Mercator.
        return 'merc'

def plot_map_earth(coordinates, full_route, length_route, name):
    # Выберите проекцию на основе координат маршрута
    projection = choose_projection(coordinates)

    # Создайте карту с выбранной проекцией
    m = Basemap(**projection, resolution='l')



    # Создаем фигуру для отображения карты
    fig = plt.figure(figsize=(8, 8))

    # Добавляем континенты
    m.drawcoastlines()
    m.drawcountries()

    # Добавляем меридианы и параллели
    m.drawmeridians(np.arange(0, 360, 30), labels=[1,0,0,1], fontsize=5)
    m.drawparallels(np.arange(-90, -66, 10), labels=[1,0,0,1], fontsize=5)

    # Добавляем точки на карту
    for point, coords in coordinates.items():
        latitude, longitude = coords
        x, y = m(longitude, latitude)
        if point == 1:
            m.plot(x, y, 'ro', markersize=5)
        else:
            m.plot(x, y, 'bo', markersize=3)
        # plt.text(x, y, f'Точка {point}', fontsize=5)
        plt.text(x, y, f'{point}', fontsize=3)

    # Добавляем маршрут на карту
    route_coordinates = [coordinates[point] for point in full_route]
    lats, lons = zip(*route_coordinates)

    x, y = m(lons, lats)
    
    m.plot(x, y, 'g--', linewidth=1)

    # Отображаем карту
    plt.title(f'Карта с точками и маршрутом. Длина маршрута-{length_route}')

    # Сохраняем карту в файл (например, PNG)
    plt.savefig(f'./image/polar_map_{name}.png', dpi=300, bbox_inches='tight')

    # Отображаем сохраненный файл
    plt.show()

