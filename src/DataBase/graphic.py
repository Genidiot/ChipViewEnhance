from typing import List
from src.DataBase.item import EntityInst


class Graphic:
    def __init__(self):
        self.device_name = ""
        self.row_count = 0
        self.column_count = 0
        self.max_row_index = 0
        self.max_column_index = 0
        self.vecEntityInst: List[EntityInst] = []

    def add_entity_inst(self, ref_entity_name, id_, logic_x, logic_y, position_):
        entity_inst = EntityInst(ref_entity_name, id_, logic_x, logic_y, position_)
        self.vecEntityInst.append(entity_inst)

    def get_entity_inst_list(self):
        return self.vecEntityInst
