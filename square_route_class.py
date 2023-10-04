class SquareRoute:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.squares = []

    def add_square(self, square):
        self.squares.append(square)

    def __str__(self):
        return f"Маршрут от точки {self.start_point} до точки {self.end_point}: {', '.join(str(square.number) for square in self.squares)}"

