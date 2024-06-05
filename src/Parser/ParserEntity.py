import json
from src.DataBase.Graphic import Graphic
from src.DataBase.Entity import Entity

class ConfigParser:
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
            entity.add_item()
        else:
            pass

