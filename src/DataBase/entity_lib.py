

class EntityLib:
    def __init__(self):
        self.mapEntity = dict()

    def __del__(self):
        for key in list(self.mapEntity.keys()):
            del self.mapEntity[key]
        self.mapEntity.clear()

    def add_entity(self, entity_name, entity):
        if entity_name not in self.mapEntity:
            self.mapEntity[entity_name] = entity

    def get_entity(self, entity_name):
        return self.mapEntity.get(entity_name)

    def get_entity_dict(self):
        return self.mapEntity


entity_lib = EntityLib()
