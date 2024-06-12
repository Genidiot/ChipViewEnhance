from typing import List
from src.DataBase.PointF import PointF


class Item:
    pass


class CircleItem(Item):
    def __init__(self, center_point: PointF, radius):
        super().__init__()
        self.centerPoint = center_point
        self.radius = radius


class LineItem(Item):
    def __init__(self, point_start: PointF, point_end: PointF):
        super().__init__()
        self.pointStart = point_start
        self.pointEnd = point_end


class PolygonItem(Item):
    def __init__(self):
        super().__init__()
        self.vecPoints: List[PointF] = []

    def add_point(self, point: PointF):
        self.vecPoints.append(point)


class PolygonLineItem(Item):
    def __init__(self):
        super().__init__()
        self.vecPoints: List[PointF] = []
