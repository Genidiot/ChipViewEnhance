class PointF:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(self, other):
            return self.x == other.column and self.y == other.row
        return False

    def set_column(self, column):
        self.x = column

    def get_column(self):
        return self.x

    def set_row(self, row):
        self.y = row

    def get_row(self):
        return self.y
