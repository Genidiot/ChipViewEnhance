from Item import Item
from typing import List


class Entity:
    def __init__(self, entity_name, level_, id_):
        self.entityName = entity_name
        self.level = level_
        self.id = id_
        self.vecItems: List[Item] = []
        