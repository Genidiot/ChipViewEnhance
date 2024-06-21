from src.DataBase import EntityLib as EntityLib_module
from src.DataBase.Entity import Entity
from ezdxf import filemanagement
from src.DataBase.Item import Item
from src.DataBase.Item import PolygonItem
from src.DataBase.Item import EntityInst
from src.DataBase.Item import CircleItem


def draw_entity(dwg, entity_name):
    entity_lib = EntityLib_module.entity_lib
    entity: Entity = entity_lib.get_entity_lib().get(entity_name)
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
        points.append((point.x, point.y))
    block.add_lwpolyline(points, close=True)


def draw_insert(item: EntityInst, block, dwg):
    ref_name = item.refEntityName
    point_x = item.position.x
    point_y = item.position.y
    draw_entity(dwg, ref_name)
    block.add_blockref(ref_name, (point_x, point_y))


def draw_circle(item: CircleItem, block):
    center_point = item.get_center_point()
    radius = item.get_radius()
    block.add_circle((center_point.x, center_point.y), radius)
