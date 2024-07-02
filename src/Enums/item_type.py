from enum import Enum, auto


class ItemType(Enum):
    ITEM_TYPE_ARC = auto()
    ITEM_TYPE_CIRCLE = auto()
    ITEM_TYPE_LINE = auto()
    ITEM_TYPE_POLYGON = auto()
    ITEM_TYPE_POLYGON_LINE = auto()
    ITEM_TYPE_TEXT = auto()
    ITEM_TYPE_ENTITY_INST = auto()
    ITEM_TYPE_UNKNOWN = auto()


str_to_item_type = {
    "Arc": ItemType.ITEM_TYPE_ARC,
    "Circle": ItemType.ITEM_TYPE_CIRCLE,
    "Line": ItemType.ITEM_TYPE_LINE,
    "Polygon": ItemType.ITEM_TYPE_POLYGON,
    "PolygonLine": ItemType.ITEM_TYPE_POLYGON_LINE,
    "Text": ItemType.ITEM_TYPE_TEXT,
    "EntityInst": ItemType.ITEM_TYPE_ENTITY_INST
}

item_type_to_str = {v: k for k, v in str_to_item_type.items()}


def item_type_str_to_enum(item_type_str: str):
    return str_to_item_type.get(item_type_str, ItemType.ITEM_TYPE_UNKNOWN)


def item_type_enum_to(item_type_enum: ItemType):
    return item_type_to_str.get(item_type_enum, "Unknown")
