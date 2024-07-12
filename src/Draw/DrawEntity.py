from src.DataBase.item import PolygonItem
from src.DataBase.item import EntityInst
from src.DataBase.item import CircleItem
from src.DataBase.entity import Entity

from src.DataBase.entity_lib import entity_lib

scale = 10


def draw_entity(dwg, entity_name):
    entity: Entity = entity_lib.get_entity(entity_name)
    if entity is None:
        return
    if dwg.blocks.get(entity.entityName) is not None:
        return
    block = dwg.blocks.new(name=entity.entityName)
    for item in entity.vecItems:
        draw_item(dwg, block, item)


def draw_item(dwg, block, item):
    if isinstance(item, PolygonItem):
        draw_polygon(item, block)
    elif isinstance(item, EntityInst):
        draw_insert(item, block, dwg)
    elif isinstance(item, CircleItem):
        draw_circle(item, block)
    else:
        pass


def draw_polygon(item: PolygonItem, block):
    points = []
    for point in item.vecPoints:
        points.append((point.x * scale, point.y * scale))
    block.add_lwpolyline(points, close=True)


def draw_insert(item: EntityInst, block, dwg):
    ref_name = item.refEntityName
    point_x = item.position.x * scale
    point_y = item.position.y * scale
    draw_entity(dwg, ref_name)
    block.add_blockref(ref_name, (point_x, point_y))


def draw_circle(item: CircleItem, block):
    center_point = item.get_center_point()
    radius = item.get_radius()
    block.add_circle((center_point.x, center_point.y), radius)
