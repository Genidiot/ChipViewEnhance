from typing import List
from src.DataBase.item import EntityInst


class Graphic:
    def __init__(self):
        self.vecEntityInst: List[EntityInst] = []

    def add_entity_inst(self, ref_entity_name, id_, logic_x, logic_y, position_):
        entity_inst = EntityInst(ref_entity_name, id_, logic_x, logic_y, position_)
        self.vecEntityInst.append(entity_inst)

    def get_entity_inst_list(self):
        return self.vecEntityInst
