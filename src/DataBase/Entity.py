from typing import List
from src.DataBase.Item import Item


class Entity:
    def __init__(self, entity_name):
        self.entityName = entity_name
        self.level = 0
        self.id = 0
        self.vecItems: List[Item] = []

    def add_item(self, item: Item):
        self.vecItems.append(item)
