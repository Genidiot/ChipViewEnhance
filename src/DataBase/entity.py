from typing import List
from src.DataBase.item import Item


class Entity:
    def __init__(self, entity_name):
        self.entityName = entity_name
        self.level = 0
        self.id = 0
        self.vecItems: List[Item] = []

    def set_entity_name(self, entity_name):
        self.entityName = entity_name

    def get_entity_name(self):
        return self.entityName

    def set_entity_level(self, level):
        self.level = level

    def get_entity_level(self):
        return self.level

    def set_entity_id(self, id_):
        self.id = id_

    def get_entity_id(self):
        return self.id

    def add_item(self, item: Item):
        self.vecItems.append(item)

    def get_items_list(self):
        return self.vecItems
