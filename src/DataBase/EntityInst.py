from PointF import PointF


class EntityInst:
    def __init__(self, ref_entity_name, id_, logic_x, logic_y, position_):
        self.refEntityName = ref_entity_name
        self.id = id_
        self.logic_x = logic_x
        self.logic_y = logic_y
        self.position: PointF = position_
