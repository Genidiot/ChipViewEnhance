from src.DataBase.item import CircleItem
from src.DataBase.item import LineItem
from src.DataBase.item import PolygonItem
from src.DataBase.item import PolygonLineItem
from src.DataBase.item import EntityInst

from src.DataBase.entity import Entity
from src.DataBase.entity_lib import entity_lib

from ezdxf.layouts import BlockLayout

scale = 1


def draw_entity(dwg, entity_type):
    entity: Entity = entity_lib.get_entity(entity_type)
    if entity is None:
        return
    if dwg.blocks.get(entity.entityName) is not None:
        return
    block: BlockLayout = dwg.blocks.new(name=entity.entityName)
    for item in entity.vecItems:
        draw_item(dwg, block, item)


def draw_item(dwg, block, item):
    if isinstance(item, CircleItem):
        draw_circle(item, block)
    elif isinstance(item, LineItem):
        draw_line(item, block)
    elif isinstance(item, PolygonItem):
        draw_polygon(item, block)
    elif isinstance(item, PolygonLineItem):
        draw_polygon_line(item, block)
    elif isinstance(item, EntityInst):
        draw_insert(item, block, dwg)
    else:
        pass


def draw_circle(item: CircleItem, block):
    center_point = item.get_center_point()
    radius = item.get_radius() * scale
    center_point_x = center_point.x * scale
    center_point_y = center_point.y * scale
    block.add_circle((center_point_x, center_point_y), radius)


def draw_line(item: LineItem, block):
    point_start = item.get_point_start()
    points_end = item.get_point_end()
    point_start_x = point_start.x * scale
    point_start_y = point_start.y * scale
    points_end_x = points_end.x * scale
    points_end_y = points_end.y * scale
    block.add_line((point_start_x, point_start_y), (points_end_x, points_end_y))


def draw_polygon(item: PolygonItem, block):
    points = []
    for point in item.vecPoints:
        point_x = point.x * scale
        point_y = point.y * scale
        points.append((point_x, point_y))
    block.add_lwpolyline(points, close=True)


def draw_polygon_line(item: PolygonLineItem, block):
    points = []
    for point in item.vecPoints:
        point_x = point.x * scale
        point_y = point.y * scale
        points.append((point_x, point_y))
    block.add_lwpolyline(points)


def draw_insert(item: EntityInst, block, dwg):
    ref_entity_type = item.entity_type
    ref_name = item.refEntityName
    point_x = item.position.x * scale
    point_y = item.position.y * scale
    draw_entity(dwg, ref_entity_type)
    ref_id = item.get_reference_id()
    rotation = item.get_rotation()
    block_ref = block.add_blockref(ref_entity_type, (point_x, point_y), dxfattribs={'rotation': rotation})
    block_ref.set_xdata("name", [(1000, ref_name)])
    block_ref.set_xdata("id", [(1071, ref_id)])
