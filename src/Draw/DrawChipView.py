import ezdxf
from ezdxf.addons import Importer

from src.ParserJson.ParserLayout import LogicRegion
from src.ParserJson.ParserLayout import ItemRegions
from src.ParserJson.ParserLayout import ChipViewLayout
from src.DataBase.graphic import chip_view_graphic

import src.Draw.DrawEntity as Draw_entity
from src.Draw import calculate_line

from typing import cast


def get_segment_length(segment_name: str):
    if segment_name[2:4] == "12":
        return 12
    elif segment_name[2:3] == "1":
        return 1
    elif segment_name[2:3] == "2":
        return 2
    elif segment_name[2:3] == "4":
        return 4
    elif segment_name[2:3] == "6":
        return 6
    elif segment_name.find("L14") != -1:
        return 14
    elif segment_name.find("L1") != -1:
        return 1
    elif segment_name.find("L2") != -1:
        return 2
    elif segment_name.find("L3") != -1:
        return 3
    elif segment_name.find("L4") != -1:
        return 4
    elif segment_name.find("L6") != -1:
        return 6
    else:
        return -1


class DxfChipView:
    def __init__(self, config: ChipViewLayout):
        self.dwg = ezdxf.new(dxfversion='AC1021')
        ezdxf.setup_linetypes(self.dwg)
        self.msp = self.dwg.modelspace()
        self.config = config
        self.insert_x = {}
        self.insert_y = {}

    def get_dwg(self):
        return self.dwg

    def get_blocks_name(self, dwg) -> list:
        block_name_list = []
        for e in dwg.blocks:
            if e.name != "*Model_Space" and e.name != "*Paper_Space":
                block_name_list.append(e.name)
        return block_name_list

    def import_block(self, sourcedwgs: list):
        for dwg in sourcedwgs:
            importer = Importer(dwg, self.dwg)
            importer.import_blocks(self.get_blocks_name(dwg))
            importer.finalize()

    def add_tile_refs(self, width, height):
        region_width = width
        region_height = height
        for item_regions in self.config.get_items_region():
            for region in item_regions.get_regions():
                for point in region.get_logic_points():
                    column = int(point.get_column())
                    row = int(point.get_row())
                    insert_x = column * region_width
                    insert_y = row * region_height
                    self.insert_x[insert_x] = column
                    self.insert_y[insert_y] = row
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

    def add_tile_ref_from_graphic(self):
        entity_inst_list = chip_view_graphic.get_entity_inst_list()
        for entity_inst in entity_inst_list:
            ref_type = entity_inst.get_ref_entity_type()
            ref_name = entity_inst.get_reference_name()
            logic_x = entity_inst.get_logic_x()
            logic_y = entity_inst.get_logic_y()
            insert_position = chip_view_graphic.logic_to_physical[(logic_x, logic_y)]
            if self.dwg.blocks.get(ref_type) is None:
                Draw_entity.draw_entity(self.dwg, ref_type)
            # If there is no entity in entity_lib, a null value is returned,
            # and add_blockref will add a null value, but no error will be reported.
            block_ref = self.msp.add_blockref(ref_type, insert_position)

    def add_segment(self, pins, line_r_list, line_l_list):
        grid = calculate_line.initialize_grid(chip_view_graphic.swh_point_map)
        grid = calculate_line.fill_grid(grid, chip_view_graphic.swh_point_map)
        for entity in self.msp:
            if entity.dxftype() == 'INSERT':
                block_ref = cast("Insert", entity)
                if block_ref.dxf.name == "SWH_W" or block_ref.dxf.name == "SWH_E":
                    insert_position = chip_view_graphic.physical_to_logic.get(
                        (block_ref.dxf.insert[0], block_ref.dxf.insert[1]))
                    distances_from_unit_e = calculate_line.calculate_logical_distances_from_unit(grid,
                                                                                                 insert_position,
                                                                                                 'x', False)
                    distances_from_unit_w = calculate_line.calculate_logical_distances_from_unit(grid,
                                                                                                 insert_position,
                                                                                                 'x', True, True)
                    distances_from_unit_n = calculate_line.calculate_logical_distances_from_unit(grid,
                                                                                                 insert_position,
                                                                                                 'y', False)
                    distances_from_unit_s = calculate_line.calculate_logical_distances_from_unit(grid,
                                                                                                 insert_position,
                                                                                                 'y', True, True)
                    # print(insert_position)
                    # print(distances_from_unit_e)
                    # print(distances_from_unit_n)
                    # print(distances_from_unit_w)
                    # print(distances_from_unit_s)
                    a_list = [1, 2, 4, 6, 12]
                    if insert_position == (13, 0):
                        pass
                    for line_length in a_list:
                        combination1 = distances_from_unit_e.get(line_length)
                        if combination1 is not None:
                            block_names = chip_view_graphic.normalLine_e_map[combination1]
                            for line_name in block_names:
                                terms = line_name.split("-")
                                start_term = terms[0]
                                pinpoint = pins[start_term]
                                line_ref = self.msp.add_blockref(line_name, block_ref.dxf.insert + pinpoint)

                        combination2 = distances_from_unit_n.get(line_length)
                        if combination2 is not None:
                            block_names = chip_view_graphic.normalLine_n_map[combination2]
                            for line_name in block_names:
                                terms = line_name.split("-")
                                start_term = terms[0]
                                pinpoint = pins[start_term]
                                line_ref = self.msp.add_blockref(line_name, block_ref.dxf.insert + pinpoint)

                        combination3 = distances_from_unit_w.get(line_length)
                        if combination3 is not None:
                            block_names = chip_view_graphic.normalLine_w_map[combination3]
                            for line_name in block_names:
                                terms = line_name.split("-")
                                start_term = terms[0]
                                pinpoint = pins[start_term]
                                line_ref = self.msp.add_blockref(line_name, block_ref.dxf.insert + pinpoint)

                        combination4 = distances_from_unit_s.get(line_length)
                        if combination4 is not None:
                            block_names = chip_view_graphic.normalLine_s_map[combination4]
                            for line_name in block_names:
                                terms = line_name.split("-")
                                start_term = terms[0]
                                pinpoint = pins[start_term]
                                line_ref = self.msp.add_blockref(line_name, block_ref.dxf.insert + pinpoint)

    def add_segment_from_graphic(self, pins, line_r_list, line_l_list):
        for entity in self.msp:
            if entity.dxftype() == 'INSERT':
                block_ref = cast("Insert", entity)
                if block_ref.dxf.name == "SWH_E":
                    insert_position = chip_view_graphic.physical_to_logic.get((block_ref.dxf.insert[0], block_ref.dxf.insert[1]))
                    logic_column = insert_position[0]
                    logic_row = insert_position[1]
                    for segment in line_l_list:
                        terms = segment.split("-")
                        start_term = terms[0]
                        pinpoint = pins[start_term]
                        segment_ref_name = self.edge_control(logic_column, logic_row, segment)
                        line_ref = self.msp.add_blockref(segment_ref_name, block_ref.dxf.insert + pinpoint)
                elif block_ref.dxf.name == "SWH_W":
                    insert_position = chip_view_graphic.physical_to_logic.get(
                        (block_ref.dxf.insert[0], block_ref.dxf.insert[1]))
                    logic_column = insert_position[0]
                    logic_row = insert_position[1]
                    for segment in line_r_list:
                        terms = segment.split("-")
                        start_term = terms[0]
                        pinpoint = pins[start_term]
                        segment_ref_name = self.edge_control(logic_column, logic_row, segment)
                        line_ref = self.msp.add_blockref(segment_ref_name, block_ref.dxf.insert + pinpoint)

    def edge_control(self, start_column, start_row, segment_name: str):
        terms = segment_name.split("-")
        start_term: str = terms[0]
        end_term: str = terms[1]
        segment_length = get_segment_length(start_term)
        if segment_length == -1:
            return segment_name

        if start_term.startswith("ee"):
            end_column = start_column + segment_length * 2 - 1
            if end_column > chip_view_graphic.get_max_column_index():
                index: int = int(segment_length - (end_column - chip_view_graphic.get_column_count() + 1) / 2)
                segment_name = start_term + "-" + end_term.replace("ee", "ww") + "-" + str(index)
        elif start_term.startswith("ww"):
            end_column = start_column - segment_length * 2 + 1
            if end_column < 0:
                index: int = int(segment_length - (0 - end_column) / 2)
                segment_name = start_term + "-" + end_term.replace("ww", "ee") + "-" + str(index)
        elif start_term.startswith("nn"):
            end_row = start_row + segment_length
            if end_row > chip_view_graphic.get_max_row_index():
                index: int = int(segment_length - (end_row - chip_view_graphic.get_row_count() + 1))
                segment_name = start_term + "-" + end_term.replace("nn", "ss") + "-" + str(index)
        elif start_term.startswith("ss"):
            end_row = start_row - segment_length
            if end_row < 0:
                index: int = int(segment_length - (0 - end_row))
                segment_name = start_term + "-" + end_term.replace("ss", "nn") + "-" + str(index)

        return segment_name

    def save_sa(self, filename: str):
        self.dwg.saveas(filename=filename)
