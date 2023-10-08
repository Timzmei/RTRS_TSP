import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def plot_map_earth(coordinates, full_route, length_route, name):
    # Создаем карту проекции полюса
    m = Basemap(projection='spstere', boundinglat=-60, lon_0=0, resolution='l')

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

