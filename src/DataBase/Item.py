from typing import List
from src.DataBase.PointF import PointF


class Item:
    pass


class CircleItem(Item):
    def __init__(self, center_point: PointF, radius):
        super().__init__()
        self.centerPoint = center_point
        self.radius = radius

    def set_center_point(self, center_point):
        self.centerPoint = center_point

    def get_center_point(self):
        return self.centerPoint

    def set_radius(self, radius):
        self.radius = radius

    def get_radius(self):
        return self.radius

    def get_type(self):
        pass


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


class EntityInst:
    def __init__(self, ref_entity_name, position_):
        super().__init__()
        self.refEntityName = ref_entity_name
        self.id = 0
        self.logic_x = 0
        self.logic_y = 0
        self.position: PointF = position_
