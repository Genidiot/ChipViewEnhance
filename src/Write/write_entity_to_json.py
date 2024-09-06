import json

from src.DataBase.entity import Entity


def entity_to_json(entity_lib) -> str:
    for entity_name, entity in entity_lib.values:
        entity: Entity
        data = {
            "Type": str
        }
        data["Type"] = entity.get_entity_name()