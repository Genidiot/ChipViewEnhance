from src.DataBase import EntityLib as EntityLib_module
from src.DataBase.Entity import Entity
from ezdxf import filemanagement
from src.DataBase.Item import Item
from src.DataBase.Item import PolygonItem


def draw_entity(dwg, entity_name):
    entity_lib = EntityLib_module.entity_lib
    entity: Entity = entity_lib.get_entity_lib().get(entity_name)
    if entity is None:
        return
    block = dwg.blocks.new(name=entity.entityName)
    for item in entity.vecItems:
        draw_item(block, item)


def draw_item(block, item):
    if isinstance(item, PolygonItem):
        draw_polygon(item, block)
    else:
        pass


def draw_polygon(item: PolygonItem, block):
    points = []
    for point in item.vecPoints:
        points.append((point.x, point.y))
    block.add_lwpolyline(points, close=True)
