import json
from src.DataBase.point import PointF
from src.DataBase.item import CircleItem
from src.DataBase.item import LineItem
from src.DataBase.item import PolygonItem
from src.DataBase.item import EntityInst
from src.DataBase.entity import Entity
from src.DataBase.graphic import Graphic
from src.Enums.item_type import ItemType, item_type_str_to_enum

from src.DataBase import entity_lib


class EntityParser:
    def __init__(self, filename):
        self.filename = filename
        self.graphic = Graphic()
        self.entity_list = list()
        self.item_list = list()
        self.entity_type = dict()

        self.__read_config()

    def __read_config(self):
        with open(self.filename, 'r') as configfile:
            configuration = json.load(configfile)
        self.__create_entity(configuration)

    def __create_entity(self, configuration: dict):
        entity_type = configuration["Type"]
        width = configuration["width"]
        height = configuration["height"]

        entity = Entity(entity_name=entity_type)

        graphic_type = item_type_str_to_enum(configuration["graphic"])
        if graphic_type == ItemType.ITEM_TYPE_ARC:
            pass
        elif graphic_type == ItemType.ITEM_TYPE_CIRCLE:
            self.item_list.append(self.create_circle(configuration["basicPoint"], configuration["radius"]))
            entity.add_item(self.item_list[-1])
        elif graphic_type == ItemType.ITEM_TYPE_LINE:
            self.item_list.append(self.create_line(configuration["polygonNodes"]))
            entity.add_item(self.item_list[-1])
        elif graphic_type == ItemType.ITEM_TYPE_POLYGON:
            self.item_list.append(self.create_polygon(configuration["polygonNodes"]))
            entity.add_item(self.item_list[-1])
        elif graphic_type == ItemType.ITEM_TYPE_POLYGON_LINE:
            pass
        else:
            pass

        if configuration.get("insideLayout"):
            for insert_item in configuration["insideLayout"]:
                item = self.create_insert(insert_item["Type"], insert_item["Name"], insert_item["pos"])
                if insert_item.get("rotation"):
                    item.set_rotation(insert_item["rotation"])
                self.item_list.append(item)
                entity.add_item(self.item_list[-1])
        if configuration.get("PinLayout"):
            for insert_item in configuration["PinLayout"]:
                self.item_list.append(self.create_insert(insert_item["Type"], insert_item["Name"], insert_item["pos"]))
                entity.add_item(self.item_list[-1])

        self.entity_list.append(entity)
        entity_library = entity_lib.entity_lib
        entity_library.add_entity(entity_type, entity)

    @staticmethod
    def create_line(line_nodes):
        point_start = PointF(line_nodes[0]["x"], line_nodes[0]["y"])
        point_end = PointF(line_nodes[1]["x"], line_nodes[1]["y"])
        line_item = LineItem(point_start, point_end)
        return line_item

    @staticmethod
    def create_polygon(polygon_nodes):
        polygon_item = PolygonItem()
        for node in polygon_nodes:
            point = PointF(node["x"], node["y"])
            polygon_item.add_point(point)
        return polygon_item

    @staticmethod
    def create_insert(ref_type, ref_name, position):
        point = PointF(position["x"], position["y"])
        entity_inst = EntityInst(ref_type, ref_name, point)
        return entity_inst

    @staticmethod
    def create_circle(basic_point, radius):
        center_point = PointF(basic_point["x"], basic_point["y"])
        circle_item = CircleItem(center_point, radius)
        return circle_item


