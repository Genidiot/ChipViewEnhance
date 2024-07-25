from src.Parser import ParserEntity
from src.Parser import ParserLayout
from src.Draw import DrawChipView
from src.Parser import ParserSWH
from src.Draw import DrawSWH
from src.Draw import DrawLine

from src.dxf import dxfblocks
from src.Draw import modify_graphic

from src.DataBase.graphic import chip_view_graphic
from src.Write import write_json

import os
import cmd
import subprocess

space = 1000


class DXFGenerator(cmd.Cmd):
    intro = 'Welcome to the DXF generator. Type help or ? to list commands.\n'
    prompt = '(dxfgen) '

    def __init__(self):
        super().__init__()
        self.effect = None
        self.dxf_content = ""
        self.config_chip_view = None
        self.chip_view = None

    def do_paser_configfile(self, filename):
        self.config_chip_view = ParserLayout.ChipViewLayout(f"./config/chipview.json")
        ParserEntity.EntityParser(f"./config/CLCL.json")
        ParserEntity.EntityParser(f"./config/SLABL_def.json")
        ParserEntity.EntityParser(f"./config/lutl_def.json")
        ParserEntity.EntityParser(f"./config/mux2_def.json")
        ParserEntity.EntityParser(f"./config/cla_def.json")
        ParserEntity.EntityParser(f"./config/swh_mux_def.json")

        chip_view = DrawChipView.DxfChipView(self.config_chip_view)
        self.chip_view = chip_view
        dwg_chip_view = chip_view.get_dwg()
        swh_l_config = ParserSWH.SwhConfig(f"./config/swhlPinLayout.json")
        swh_l = DrawSWH.SwhCreate(swh_l_config, dwg_chip_view)
        pins = swh_l.get_sub_block_dict()
        swh_r_config = ParserSWH.SwhConfig(f"./config/swhrPinLayout.json")
        swh_r = DrawSWH.SwhCreate(swh_r_config, dwg_chip_view)

        segments = dxfblocks.DxfBlocks(f"./import_dxf")
        segment_dwg = segments.get_dwgs()
        chip_view.import_block(segment_dwg)

        normal_line = DrawLine.NormalLineCreate(swh_l_config, swh_l, dwg_chip_view, space)
        normal_line.create_line()
        line_l = normal_line.get_line_l_list()
        line_r = normal_line.get_line_r_list()

        # chip_view.add_tile_refs(width, height)
        chip_view.add_tile_ref_from_graphic()
        # chip_view.add_segment(pins, line_r, line_l)
        chip_view.add_segment_from_graphic(pins, line_r, line_l)

    def do_set_effect(self, arg):
        modify_graphic.modify_graphic()

    def do_generate_dxf(self, arg):
        self.chip_view.save_sa(f"./result_dxf/test3.dxf")

    def do_exit(self, arg):
        'Exit the DXF generator'
        print('Goodbye!')
        return True

    def generate_effect(self):
        self.chip_view.save_sa(f"./result_dxf/test3.dxf")

def create_tc():
    # config_chip_view = ParserLayout.ChipViewLayout(f"./config/chipview.json")
    config_chip_view = ParserLayout.ChipViewLayout(f"output.json")
    # ParserEntity.EntityParser(f"./config/SWHL.json")
    ParserEntity.EntityParser(f"./config/CLCL.json")
    ParserEntity.EntityParser(f"./config/SLABL_def.json")
    ParserEntity.EntityParser(f"./config/lutl_def.json")
    ParserEntity.EntityParser(f"./config/mux2_def.json")
    ParserEntity.EntityParser(f"./config/cla_def.json")
    ParserEntity.EntityParser(f"./config/swh_mux_def.json")

    chip_view = DrawChipView.DxfChipView(config_chip_view)
    dwg_chip_view = chip_view.get_dwg()
    swh_l_config = ParserSWH.SwhConfig(f"./config/swhlPinLayout.json")
    swh_l = DrawSWH.SwhCreate(swh_l_config, dwg_chip_view)
    pins = swh_l.get_sub_block_dict()
    swh_r_config = ParserSWH.SwhConfig(f"./config/swhrPinLayout.json")
    swh_r = DrawSWH.SwhCreate(swh_r_config, dwg_chip_view)

    modify_graphic.modify_graphic()

    segments = dxfblocks.DxfBlocks(f"./import_dxf")
    segment_dwg = segments.get_dwgs()
    chip_view.import_block(segment_dwg)

    normal_line = DrawLine.NormalLineCreate(swh_l_config, swh_l, dwg_chip_view, space)
    normal_line.create_line()
    line_l = normal_line.get_line_l_list()
    line_r = normal_line.get_line_r_list()

    # chip_view.add_tile_refs(width, height)
    chip_view.add_tile_ref_from_graphic()
    # chip_view.add_segment(pins, line_r, line_l)
    chip_view.add_segment_from_graphic(pins, line_r, line_l)
    chip_view.save_sa(f"./result_dxf/test3.dxf")

    # json_output = write_json.graphic_to_json(chip_view_graphic)
    # write_json.save_json_to_file(json_output, 'output.json')


if __name__ == '__main__':
    DXFGenerator().cmdloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# 规则
# class name        PascalCase
# module/file name  snake_case
# function          snake_case
# 私有变量            snake_case
# 函数参数            snake_case
