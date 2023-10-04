class Square:
    def __init__(self, number, min_latitude, max_latitude, min_longitude, max_longitude):
        self.number = number
        self.min_latitude = min_latitude
        self.max_latitude = max_latitude
        self.min_longitude = min_longitude
        self.max_longitude = max_longitude
        self.start_point_inside = None
        self.end_point_inside = None
        self.points_inside = []
        self.connected_squares = []
        self.parent_square = None  # Добавляем поле "материнский квадрат"

    def set_start_point_inside(self, point):
        self.start_point_inside = point

    def set_end_point_inside(self, point):
        self.end_point_inside = point

    def add_point_inside(self, point):
        self.points_inside.append(point)

    def add_connected_square(self, square):
        self.connected_squares.append(square)

    def set_parent_square(self, parent_square):
        self.parent_square = parent_square
        
    def calculate_center(self):
        center_lat = (self.min_latitude + self.max_latitude) / 2
        center_lon = (self.min_longitude + self.max_longitude) / 2
        return (center_lat, center_lon)