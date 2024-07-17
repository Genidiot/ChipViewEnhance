import json
from src.DataBase.graphic import Graphic

class LayoutParser:
    def __init__(self, filename):
        self.filename = filename

        self.__read_config()

    def __read_config(self):
        with open(self.filename, 'r') as configfile:
            configuration = json.load(configfile)
        self.__parser_config(configuration)

    def __parser_config(self, configuration: dict):
        self.device_name = configuration["deviceName"]