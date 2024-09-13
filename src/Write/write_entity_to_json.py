from src.DataBase.item import CircleItem
from src.DataBase.item import LineItem
from src.DataBase.item import PolygonItem
from src.DataBase.item import PolygonLineItem
from src.DataBase.item import EntityInst

from src.DataBase.entity import Entity
from src.DataBase.entity_lib import entity_lib

from src.Enums.item_type import item_type_enum_to_str
import json
import os


def entity_to_json():
    for entity_name, entity in entity_lib.get_entity_dict().items():
        entity_dict = convert_entity_to_dict(entity)
        save_entity_to_file(entity_name, entity_dict)


def convert_entity_to_dict(entity: Entity):
    entity_dict = {
        "Type": entity.get_entity_name(),
        "width": 0,  # Placeholder, modify as needed
        "height": 0,  # Placeholder, modify as needed
        "basicPoint": {"x": 0, "y": 0},  # Placeholder, modify as needed
        "items": [],
        "PinObjects": [],
        "PinLayout": [],
        "insideObjects": [],
        "insideLayout": [],
        "LineObjects": [],
        "LineLayout": []
    }

    # Process the items in the entity
    for item in entity.get_items_list():
        if isinstance(item, CircleItem):
            entity_dict["items"].append(convert_circle_to_dict(item))
        elif isinstance(item, LineItem):
            entity_dict["items"].append(convert_line_to_dict(item))
        elif isinstance(item, PolygonItem):
            entity_dict["items"].append(convert_polygon_to_dict(item))
        elif isinstance(item, PolygonLineItem):
            entity_dict["items"].append(convert_polygon_line_to_dict(item))
        elif isinstance(item, EntityInst):
            if item.get_ref_entity_type().startswith("circle_pin") \
                    or item.get_ref_entity_type().startswith("left_pin") \
                    or item.get_ref_entity_type().startswith("right_pin") \
                    or item.get_ref_entity_type().startswith("up_pin") \
                    or item.get_ref_entity_type().startswith("down_pin"):
                entity_dict["PinObjects"].append(convert_item_object_to_dict(item))
                entity_dict["PinLayout"].append(convert_item_layout_to_dict(item))
            elif item.get_ref_entity_type().startswith("line"):
                entity_dict["LineObjects"].append(convert_item_object_to_dict(item))
                entity_dict["LineLayout"].append(convert_item_layout_to_dict(item))
            else:
                entity_dict["insideObjects"].append(convert_item_object_to_dict(item))
                entity_dict["insideLayout"].append(convert_item_layout_to_dict(item))

    if not entity_dict["insideObjects"]:
        del entity_dict["insideObjects"]
    if not entity_dict["insideLayout"]:
        del entity_dict["insideLayout"]
    if not entity_dict["PinObjects"]:
        del entity_dict["PinObjects"]
    if not entity_dict["PinLayout"]:
        del entity_dict["PinLayout"]
    if not entity_dict["LineObjects"]:
        del entity_dict["LineObjects"]
    if not entity_dict["LineLayout"]:
        del entity_dict["LineLayout"]

    return entity_dict


def convert_circle_to_dict(circle_item: CircleItem):
    return {
        "graphic": item_type_enum_to_str(circle_item.get_item_type()),
        "radius": int(circle_item.get_radius()),
        "connectPoint": {"x": int(circle_item.get_center_point().x),
                         "y": int(circle_item.get_center_point().y)}
    }


def convert_line_to_dict(line_item: LineItem):
    return {
        "graphic": item_type_enum_to_str(line_item.get_item_type()),
        "polygonNodes": [
            {"x": int(line_item.get_point_start().x), "y": int(line_item.get_point_start().y)},
            {"x": int(line_item.get_point_end().x), "y": int(line_item.get_point_end().y)}
        ]
    }


def convert_polygon_to_dict(polygon_item: PolygonItem):
    return {
        "graphic": item_type_enum_to_str(polygon_item.get_item_type()),
        "polygonNodes": [{"x": int(point.x), "y": int(point.y)} for point in polygon_item.get_points_list()]
    }


def convert_polygon_line_to_dict(polygon_line_item: PolygonLineItem):
    return {
        "graphic": item_type_enum_to_str(polygon_line_item.get_item_type()),
        "polygonNodes": [{"x": int(point.x), "y": int(point.y)} for point in polygon_line_item.get_points_list()]
    }


def convert_item_object_to_dict(insert_item):
    return {
        "Type": insert_item.get_ref_entity_type(),
        "Name": insert_item.get_reference_name(),
        "id": insert_item.get_reference_id() if insert_item.get_reference_id() else 0,
        "rotation": int(insert_item.get_rotation()) if insert_item.get_rotation() else 0
    }


def convert_item_layout_to_dict(insert_item):
    return {
        "Name": insert_item.get_reference_name(),
        "pos": {
            "x": int(insert_item.get_position().x),
            "y": int(insert_item.get_position().y)
        }
    }


def save_entity_to_file(entity_name, entity_dict):
    # Generate filename based on entity name
    output_directory = "./output_json"
    filename = f"def_{entity_name}.json"
    filepath = os.path.join(output_directory, filename)

    # Write JSON data to file
    with open(filepath, 'w') as json_file:
        json.dump(entity_dict, json_file, indent=4)

    print(f"Entity {entity_name} has been exported to {filepath}")
