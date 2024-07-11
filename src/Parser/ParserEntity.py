import json
from src.DataBase.point import PointF
from src.DataBase.item import PolygonItem
from src.DataBase.entity import Entity
from src.DataBase.graphic import Graphic
from src.DataBase.item import EntityInst
from src.DataBase.item import CircleItem

from src.DataBase import entity_lib
from src.DataBase.entity_lib import EntityLib


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
        entity_type = configuration["tileType"]
        width = configuration["width"]
        height = configuration["height"]

        entity = Entity(entity_name=entity_type)

        graphic_type = configuration["graphic"]
        if graphic_type == "LINE":
            pass
        elif graphic_type == "CIRCLE":
            self.item_list.append(self.create_circle(configuration["basicPoint"], configuration["radius"]))
            entity.add_item(self.item_list[-1])
        elif graphic_type == "POLYGON":
            self.item_list.append(self.create_polygon(configuration["polygonNodes"]))
            entity.add_item(self.item_list[-1])
        else:
            pass

        if configuration.get("insideLayout"):
            for insert_item in configuration["insideLayout"]["Layout"]:
                self.item_list.append(self.create_insert(insert_item["siteBlock"], insert_item["pos"]))
                entity.add_item(self.item_list[-1])
        if configuration.get("muxLayout"):
            for insert_item in configuration["muxLayout"]["position"]:
                self.item_list.append(self.create_insert(insert_item["pinName"], insert_item["startPos"]))
                entity.add_item(self.item_list[-1])

        self.entity_list.append(entity)
        entity_library = entity_lib.entity_lib
        entity_library.add_entity(entity_type, entity)

    def create_polygon(self, polygon_nodes):
        polygon_item = PolygonItem()
        for node in polygon_nodes:
            point = PointF(node["x"], node["y"])
            polygon_item.add_point(point)
        return polygon_item

    def create_insert(self, ref_name, position):
        point = PointF(position["x"], position["y"])
        entity_inst = EntityInst(ref_name, point)
        return entity_inst

    def create_circle(self, basic_point, radius):
        center_point = PointF(basic_point["x"], basic_point["y"])
        circle_item = CircleItem(center_point, radius)
        return circle_item


