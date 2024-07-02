from typing import List

from src.DataBase.point import PointF

from src.Enums.item_type import ItemType


class Item:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def get_item_type(self):
        return ItemType.ITEM_TYPE_UNKNOWN


class CircleItem(Item):
    def __init__(self, center_point: PointF, radius):
        super().__init__()
        self.center_point = center_point
        self.radius = radius

    def set_center_point(self, center_point):
        self.center_point = center_point

    def get_center_point(self):
        return self.center_point

    def set_radius(self, radius):
        self.radius = radius

    def get_radius(self):
        return self.radius

    def get_item_type(self):
        return ItemType.ITEM_TYPE_CIRCLE


class LineItem(Item):
    def __init__(self, point_start: PointF, point_end: PointF):
        super().__init__()
        self.point_start = point_start
        self.point_end = point_end

    def set_point_start(self, point_start):
        self.point_start = point_start

    def get_point_start(self):
        return self.point_start

    def set_point_end(self, point_end):
        self.point_end = point_end

    def get_point_end(self):
        return self.point_end

    def get_item_type(self):
        return ItemType.ITEM_TYPE_LINE


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
