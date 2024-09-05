import json
from src.DataBase.graphic import Graphic
from src.DataBase.item import EntityInst


def graphic_to_json(graphic: Graphic) -> str:
    data = {
        "deviceName": graphic.get_device_name(),
        "rowNum": graphic.get_row_count(),
        "colNum": graphic.get_column_count(),
        "rowHeights": {str(k): v for k, v in graphic.row_heights.items()},
        "columnWidths": {str(k): v for k, v in graphic.column_widths.items()},
        "itemRegion": []
    }

    # 生成 itemRegion 部分
    type_to_regions = {}
    for entity_inst in graphic.get_entity_inst_list():
        entity_inst: EntityInst
        entity_type = entity_inst.refEntityName
        if entity_type not in type_to_regions:
            type_to_regions[entity_type] = {
                "type": entity_type,
                "width": 1,
                "height": 1,
                "regions": []
            }
        type_to_regions[entity_type]["regions"].append({
            "startX": entity_inst.logic_x,
            "startY": entity_inst.logic_y,
            "endX": entity_inst.logic_x,
            "endY": entity_inst.logic_y
        })

    data["itemRegion"] = list(type_to_regions.values())

    json_str = json.dumps(data, indent=4)
    return json_str


def save_json_to_file(json_str: str, filename: str):
    with open(filename, 'w') as file:
        file.write(json_str)
