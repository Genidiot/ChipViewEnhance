import json
from src.DataBase.PointF import PointF
from src.DataBase.Item import PolygonItem
from src.DataBase.Entity import Entity
from src.DataBase.Graphic import Graphic

from src.DataBase.EntityLib import EntityLib
import src.DataBase.EntityLib as EntityLib_module


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
            pass
        elif graphic_type == "POLYGON":
            self.item_list.append(self.create_polygon(configuration["polygonNodes"]))
            entity.add_item(self.item_list[-1])
        else:
            pass

        self.entity_list.append(entity)
        entity_lib = EntityLib_module.entity_lib
        entity_lib.add_entity(entity_type, entity)

    def create_polygon(self, polygon_nodes):
        polygon_item = PolygonItem()
        for node in polygon_nodes:
            point = PointF(node["x"], node["y"])
            polygon_item.add_point(point)
        return polygon_item


