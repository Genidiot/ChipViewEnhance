from src.DataBase.item import CircleItem
from src.DataBase.item import LineItem
from src.DataBase.item import PolygonItem
from src.DataBase.item import PolygonLineItem
from src.DataBase.item import EntityInst
from src.DataBase.item import TextItem
from src.DataBase.entity import Entity
from src.DataBase.entity_lib import entity_lib
from src.DataBase.point import PointF

from ezdxf.layouts import BlockLayout
from ezdxf.entities import Circle
from ezdxf.entities import Line
from ezdxf.entities import LWPolyline
from ezdxf.entities import Insert
from ezdxf.entities import Text
from ezdxf.entities import Attrib

from typing import cast

insert_map = {}


def write_blocks(dwg):
    for block in dwg.blocks:
        if block.name == "*Model_Space" or block.name == "*Paper_Space" or block.name == "*Paper_Space0":
            continue
        dxf_block_to_data(block)


def dxf_block_to_data(dxf_block: BlockLayout):
    entity = Entity(dxf_block.name)

    if dxf_block.block.has_xdata("level"):
        tags = dxf_block.block.get_xdata("level")
        for tag in tags:
            entity.set_entity_level(tag[1])
    if dxf_block.block.has_xdata("id"):
        tags = dxf_block.block.get_xdata("id")
        for tag in tags:
            entity.set_entity_id(tag[1])

    for dxf_entity in dxf_block:
        if dxf_entity.dxftype() == "CIRCLE":
            dxf_circle = cast("Circle", dxf_entity)
            item_circle = dxf_circle_to_data(dxf_circle)
            entity.add_item(item_circle)
        elif dxf_entity.dxftype() == "LINE":
            dxf_line = cast("Line", dxf_entity)
            item_line = dxf_line_to_data(dxf_line)
            entity.add_item(item_line)
        elif dxf_entity.dxftype() == "LWPOLYLINE":
            dxf_polyline = cast("LWPolyline", dxf_entity)
            item_polyline = dxf_polyline_to_data(dxf_polyline)
            entity.add_item(item_polyline)
        elif dxf_entity.dxftype() == "TEXT":
            dxf_text = cast("Text", dxf_entity)
            item_text = dxf_text_to_data(dxf_text)
            entity.add_item(item_text)
        elif dxf_entity.dxftype() == "INSERT":
            dxf_insert = cast("Insert", dxf_entity)
            item_entity_inst = dxf_insert_to_data(dxf_insert)
            insert_map[dxf_insert.dxf.insert] = item_entity_inst
            entity.add_item(item_entity_inst)
        elif dxf_entity.dxftype() == "ATTRIB":
            dxf_attrib = cast("Attrib", dxf_entity)
            attrib_position = dxf_attrib.dxf.insert
            item_entity_inst = insert_map[attrib_position]
            dxf_attrib_add_to_insert(dxf_attrib, item_entity_inst)
        else:
            pass

    entity_lib.add_entity(dxf_block.name, entity)


def dxf_circle_to_data(dxf_circle: Circle):
    if dxf_circle is None:
        return None
    center_point = PointF(dxf_circle.dxf.center.x, dxf_circle.dxf.center.y)
    radius = dxf_circle.dxf.radius
    item_circle = CircleItem(center_point, radius)

    return item_circle


def dxf_line_to_data(dxf_line: Line):
    if dxf_line is None:
        return None
    point_start = PointF(dxf_line.dxf.start.x, dxf_line.dxf.start.y)
    point_end = PointF(dxf_line.dxf.end.x, dxf_line.dxf.end.y)
    item_line = LineItem(point_start, point_end)

    return item_line


def dxf_polyline_to_data(dxf_polyline: LWPolyline):
    if dxf_polyline is None:
        return None
    if dxf_polyline.is_closed:
        item_polyline = PolygonItem()
    else:
        item_polyline = PolygonLineItem()

    dxf_polyline_points = dxf_polyline.get_points()
    for dxf_point in dxf_polyline_points:
        item_point = PointF(dxf_point[0], dxf_point[1])
        item_polyline.add_point(item_point)

    return item_polyline


def dxf_text_to_data(dxf_text: Text):
    if dxf_text is None:
        return None
    text = dxf_text.dxf.text
    position = PointF(dxf_text.dxf.insert.x, dxf_text.dxf.insert.y)
    # direction = int(dxf_text.dxf.rotation)
    item_text = TextItem(text, position)

    return item_text


def dxf_insert_to_data(dxf_insert: Insert):
    if dxf_insert is None:
        return None
    ref_type = dxf_insert.dxf.name
    ref_name = None
    ref_id = None
    if dxf_insert.has_attrib("name"):
        ref_name = dxf_insert.get_attrib("name").dxf.text
    if dxf_insert.has_attrib("id"):
        ref_id = int(dxf_insert.get_attrib("id").dxf.text)
    rotation = dxf_insert.get_dxf_attrib("rotation")
    position = PointF(dxf_insert.dxf.insert.x, dxf_insert.dxf.insert.y)
    item_entity_inst = EntityInst(ref_type, ref_name, position, id_=ref_id, rotation=rotation)

    return item_entity_inst


def dxf_attrib_add_to_insert(dxf_attrib: Attrib, item_entity_inst: EntityInst):
    if dxf_attrib.dxf.tag == "name":
        ref_name = dxf_attrib.dxf.text
        item_entity_inst.set_reference_name(ref_name)
    elif dxf_attrib.dxf.tag == "id":
        ref_id = int(dxf_attrib.dxf.text)
        item_entity_inst.set_reference_id(ref_id)
