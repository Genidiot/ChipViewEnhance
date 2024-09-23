from src.DataBase.item import CircleItem
from src.DataBase.item import LineItem
from src.DataBase.item import PolygonItem
from src.DataBase.item import PolygonLineItem
from src.DataBase.item import EntityInst

from src.DataBase.entity import Entity
from src.DataBase.entity_lib import entity_lib
from src.DataBase.point import PointF

from src.Enums.item_type import ItemType, item_type_str_to_enum
import json


class EntityParser:
    def __init__(self, filename):
        self.filename = filename
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

        for graphic_item in configuration["items"]:
            graphic_type = item_type_str_to_enum(graphic_item["graphic"])
            if graphic_type == ItemType.ITEM_TYPE_ARC:
                pass
            elif graphic_type == ItemType.ITEM_TYPE_CIRCLE:
                self.item_list.append(self.create_circle(graphic_item["connectPoint"], graphic_item["radius"]))
                entity.add_item(self.item_list[-1])
            elif graphic_type == ItemType.ITEM_TYPE_LINE:
                self.item_list.append(self.create_line(graphic_item["polygonNodes"]))
                entity.add_item(self.item_list[-1])
            elif graphic_type == ItemType.ITEM_TYPE_POLYGON:
                self.item_list.append(self.create_polygon(graphic_item["polygonNodes"]))
                entity.add_item(self.item_list[-1])
            elif graphic_type == ItemType.ITEM_TYPE_POLYGON_LINE:
                self.item_list.append(self.create_polygon_line(graphic_item["polygonNodes"]))
                entity.add_item(self.item_list[-1])
            else:
                pass

        if configuration.get("insideLayout") and configuration.get("insideObjects"):
            inside_objects = {obj["Name"]: obj for obj in configuration["insideObjects"]}
            for insert_item in configuration["insideLayout"]:
                item_info = inside_objects.get(insert_item["Name"])
                self.item_list.append(self.create_insert(item_info["Type"],
                                                         item_info["Name"],
                                                         item_info["id"],
                                                         item_info["rotation"],
                                                         insert_item["pos"]))
                entity.add_item(self.item_list[-1])
        if configuration.get("PinLayout") and configuration.get("PinObjects"):
            pin_objects = {obj["Name"]: obj for obj in configuration["PinObjects"]}
            for insert_item in configuration["PinLayout"]:
                item_info = pin_objects.get(insert_item["Name"])
                self.item_list.append(self.create_insert(item_info["Type"],
                                                         item_info["Name"],
                                                         item_info["id"],
                                                         item_info["rotation"],
                                                         insert_item["pos"]))
                entity.add_item(self.item_list[-1])
        if configuration.get("LineLayout") and configuration.get("LineObjects"):
            pin_objects = {obj["Name"]: obj for obj in configuration["LineObjects"]}
            for insert_item in configuration["LineLayout"]:
                item_info = pin_objects.get(insert_item["Name"])
                self.item_list.append(self.create_insert(item_info["Type"],
                                                         item_info["Name"],
                                                         item_info["id"],
                                                         item_info["rotation"],
                                                         insert_item["pos"]))
                entity.add_item(self.item_list[-1])

        self.entity_list.append(entity)
        entity_lib.add_entity(entity_type, entity)

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
    def create_polygon_line(polygon_line_nodes):
        polygon_line_item = PolygonLineItem()
        for node in polygon_line_nodes:
            point = PointF(node["x"], node["y"])
            polygon_line_item.add_point(point)
        return polygon_line_item

    @staticmethod
    def create_insert(ref_type, ref_name, ref_id, rotation,  position):
        point = PointF(position["x"], position["y"])
        entity_inst = EntityInst(ref_type, ref_name, point, id_=ref_id, rotation=rotation)
        return entity_inst

    @staticmethod
    def create_circle(basic_point, radius):
        center_point = PointF(basic_point["x"], basic_point["y"])
        circle_item = CircleItem(center_point, radius)
        return circle_item
