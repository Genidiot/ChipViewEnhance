import ezdxf

from src.Parser.ParserLayout import LogicRegion
from src.Parser.ParserLayout import ItemRegions
from src.Parser.ParserLayout import ChipViewLayout

import src.Draw.DrawEntity as Draw_entity


class DxfChipView:
    def __init__(self, config: ChipViewLayout):
        self.dwg = ezdxf.new(dxfversion='AC1021')
        ezdxf.setup_linetypes(self.dwg)
        self.msp = self.dwg.modelspace()
        self.config = config

    def add_tile_refs(self):
        region_width = 500
        region_height = 500
        for item_regions in self.config.get_items_region():
            for region in item_regions.get_regions():
                for point in region.get_logic_points():
                    column = int(point.get_column())
                    row = int(point.get_row())
                    insert_x = column * region_width
                    insert_y = row * region_height
                    tile_type = item_regions.get_item_type()
                    if self.dwg.blocks.get(tile_type) is None:
                        Draw_entity.draw_entity(self.dwg, tile_type)

                    block_ref = self.msp.add_blockref(
                        tile_type,
                        (
                            insert_x,
                            insert_y
                        )
                    )

    def save_sa(self, filename: str):
        self.dwg.saveas(filename=filename)