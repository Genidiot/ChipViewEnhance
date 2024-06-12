

class EntityLib:
    def __init__(self):
        self.mapEntity = dict()

    def add_entity(self, entity_name, entity):
        if entity_name not in self.mapEntity:
            self.mapEntity[entity_name] = entity

    def get_entity_lib(self):
        return self.mapEntity


entity_lib = EntityLib()
