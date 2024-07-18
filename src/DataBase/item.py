from typing import List

from src.DataBase.point import PointF

from src.Enums.item_type import ItemType
from src.Enums.text_direction import TextDirection


class Item:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def render(self):
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

    def get_points_list(self):
        return self.vecPoints

    def get_item_type(self):
        return ItemType.ITEM_TYPE_POLYGON


class PolygonLineItem(Item):
    def __init__(self):
        super().__init__()
        self.vecPoints: List[PointF] = []

    def add_point(self, point: PointF):
        self.vecPoints.append(point)

    def get_points_list(self):
        return self.vecPoints

    def get_item_type(self):
        return ItemType.ITEM_TYPE_POLYGON_LINE


class TextItem(Item):
    def __init__(self, text: str, position: PointF, direction: TextDirection):
        super().__init__()
        self.text = text
        self.position = position
        self.direction = direction

    def set_text(self, text: str):
        self.text = text

    def get_text(self):
        return self.text

    def set_position(self, position: PointF):
        self.position = position

    def get_position(self):
        return self.position

    def set_direction(self, direction: TextDirection):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def get_item_type(self):
        return ItemType.ITEM_TYPE_TEXT


class EntityInst(Item):
    def __init__(self, ref_entity_name, position_, logic_x=None, logic_y=None, id_=None):
        super().__init__()
        self.refEntityName = ref_entity_name
        self.id = id_
        self.logic_x = logic_x
        self.logic_y = logic_y
        self.position: PointF = position_

    def set_reference_name(self, ref_entity_name: str):
        self.refEntityName = ref_entity_name

    def get_reference_name(self):
        return self.refEntityName

    def set_reference_id(self, id_):
        self.id = id_

    def get_reference_id(self):
        return self.id

    def set_logic_x(self, logic_x):
        self.logic_x = logic_x

    def get_logic_x(self):
        return self.logic_x

    def set_logic_y(self, logic_y):
        self.logic_y = logic_y

    def get_logic_y(self):
        return self.logic_y

    def set_position(self, position: PointF):
        self.position = position

    def get_position(self):
        return self.position

    def get_item_type(self):
        return ItemType.ITEM_TYPE_ENTITY_INST

    def render(self):
        return f"Rendering {self.refEntityName} at logical ({self.logic_x}, {self.logic_y}, position{self.position})"
