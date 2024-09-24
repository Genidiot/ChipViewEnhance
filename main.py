from src.ParserJson import ParserLayout
from src.ParserJson import ParserEntity
from src.ParserJson import ParserSWH
from src.ParserJson import ParserLine
from src.Draw import DrawSWH
from src.Draw import DrawLine
from src.Draw import DrawLine2
from src.Draw import DrawChipView

from src.ParserDxf import dxfblocks
from src.Draw import modify_graphic

from src.DataBase.graphic import chip_view_graphic
from src.Write import write_graphic_to_json

import os
import cmd
import subprocess
import ezdxf
import src.Draw.DrawEntity as Draw_entity
from src.ParserDxf import dxf_to_data
from src.Write import write_entity_to_json
from src.ParserJson import find_files

space = 1000


# class DXFGenerator(cmd.Cmd):
#     intro = 'Welcome to the DXF generator. Type help or ? to list commands.\n'
#     prompt = '(dxfgen) '
#
#     def __init__(self):
#         super().__init__()
#         self.effect = None
#         self.dxf_content = ""
#         self.config_chip_view = None
#         self.chip_view = None
#
#     def do_paser_configfile(self, filename):
#         self.config_chip_view = ParserLayout.ChipViewLayout(f"./config/chipview.json")
#         ParserEntity.EntityParser(f"./config/CLCL.json")
#         ParserEntity.EntityParser(f"./config/SLABL_def.json")
#         ParserEntity.EntityParser(f"./config/lutl_def.json")
#         ParserEntity.EntityParser(f"./config/mux2_def.json")
#         ParserEntity.EntityParser(f"./config/cla_def.json")
#         ParserEntity.EntityParser(f"./config/swh_mux_def.json")
#
#         chip_view = DrawChipView.DxfChipView(self.config_chip_view)
#         self.chip_view = chip_view
#         dwg_chip_view = chip_view.get_dwg()
#         swh_l_config = ParserSWH.SwhConfig(f"./config/swhlPinLayout.json")
#         swh_l = DrawSWH.SwhCreate(swh_l_config, dwg_chip_view)
#         pins = swh_l.get_sub_block_dict()
#         swh_r_config = ParserSWH.SwhConfig(f"./config/swhrPinLayout.json")
#         swh_r = DrawSWH.SwhCreate(swh_r_config, dwg_chip_view)
#
#         segments = dxfblocks.DxfBlocks(f"./import_dxf")
#         segment_dwg = segments.get_dwgs()
#         chip_view.import_block(segment_dwg)
#
#         normal_line = DrawLine.NormalLineCreate(swh_l_config, swh_l, dwg_chip_view, space)
#         normal_line.create_line()
#         line_l = normal_line.get_line_l_list()
#         line_r = normal_line.get_line_r_list()
#
#         # chip_view.add_tile_refs(width, height)
#         chip_view.add_tile_ref_from_graphic()
#         # chip_view.add_segment(pins, line_r, line_l)
#         chip_view.add_segment_from_graphic(pins, line_r, line_l)
#
#     def do_set_effect(self, arg):
#         modify_graphic.modify_graphic()
#
#     def do_generate_dxf(self, arg):
#         self.chip_view.save_sa(f"./result_dxf/test3.dxf")
#
#     def do_exit(self, arg):
#         'Exit the DXF generator'
#         print('Goodbye!')
#         return True
#
#     def generate_effect(self):
#         self.chip_view.save_sa(f"./result_dxf/test3.dxf")


# def create_tc_test1():
#     ParserEntity.EntityParser(f"./config/def_CLCL.json")
#     ParserEntity.EntityParser(f"./config/def_SLAB.json")
#     ParserEntity.EntityParser(f"./config/def_cla.json")
#     ParserEntity.EntityParser(f"./config/def_lutl.json")
#     ParserEntity.EntityParser(f"./config/def_mux2.json")
#     ParserEntity.EntityParser(f"./config/def_mux4.json")
#     ParserEntity.EntityParser(f"./config/def_muxf.json")
#     ParserEntity.EntityParser(f"./config/def_pin_up.json")
#     ParserEntity.EntityParser(f"./config/def_pin_down.json")
#     ParserEntity.EntityParser(f"./config/def_pin_left.json")
#     ParserEntity.EntityParser(f"./config/def_pin_right.json")
#     ParserEntity.EntityParser(f"./config/def_pin_circle.json")
#
#     config_chip_view = ParserLayout.ChipViewLayout(f"./config/chipview.json")
#     # config_chip_view = ParserLayout.ChipViewLayout(f"output.json")
#     chip_view = DrawChipView.DxfChipView(config_chip_view)
#     dwg_chip_view = chip_view.get_dwg()
#
#     swh_l_config = ParserSWH.SwhConfig(f"./config/SWH_W.json")
#     swh_l = DrawSWH.SwhCreate(swh_l_config, dwg_chip_view)
#     pins = swh_l.get_sub_block_dict()
#     swh_r_config = ParserSWH.SwhConfig(f"./config/SWH_E.json")
#     swh_r = DrawSWH.SwhCreate(swh_r_config, dwg_chip_view)
#
#     # modify_graphic.modify_graphic()
#
#     # segments = dxfblocks.DxfBlocks(f"./import_dxf")
#     # segment_dwg = segments.get_dwgs()
#     # chip_view.import_block(segment_dwg)
#
#     normal_line = DrawLine2.NormalLineCreate(swh_l_config, swh_l, dwg_chip_view, space)
#     normal_line.create_line()
#     line_l = normal_line.get_line_l_list()
#     line_r = normal_line.get_line_r_list()
#
#     # chip_view.add_tile_refs(width, height)
#     chip_view.add_tile_ref_from_graphic()
#     chip_view.add_segment(pins)
#     # chip_view.add_segment_from_graphic(pins, line_r, line_l)
#     chip_view.save_sa(f"./result_dxf/test3.dxf")
#
#     # json_output = write_json.graphic_to_json(chip_view_graphic)
#     # write_json.save_json_to_file(json_output, 'output.json')


def create_tc_test2():
    find_files.read_entity_files(f"./config/config_entity")

    config_chip_view = ParserLayout.ChipViewLayout(f"./config/config_view/chipview.json")
    chip_view = DrawChipView.DxfChipView(config_chip_view)

    ParserSWH.SwhConfig(f"./config/config_swh/SWH_E.json")
    swh_l_config = ParserSWH.SwhConfig(f"./config/config_swh/SWH_W.json")
    pins = swh_l_config.get_sub_block_dict()

    # modify_graphic.modify_graphic()
    # segments = dxfblocks.DxfBlocks(f"./import_dxf")
    # segment_dwg = segments.get_dwgs()
    # chip_view.import_block(segment_dwg)

    line_config = ParserLine.LineConfig(f"./config/config_swh/template_line.json")
    line_config.create_line_entity(swh_l_config)

    chip_view.add_tile_ref_from_graphic()
    chip_view.add_segment(pins)
    chip_view.save_sa(f"./result_dxf/test3.dxf")

    # json_output = write_json.graphic_to_json(chip_view_graphic)
    # write_json.save_json_to_file(json_output, 'output.json')


def block_import_test():
    read_prototype_entity_config(f"./config/config_entity")
    output_prototype_dxf("CLCL")


def block_output_test():
    read_prototype_dxf(f"./output_dxf")
    write_entity_to_json.entity_to_json()


def read_prototype_entity_config(directory):
    find_files.read_entity_files(directory)


def output_prototype_dxf(entity_type):
    dwg = ezdxf.new(dxfversion='AC1021')
    Draw_entity.draw_entity(dwg, entity_type)
    dwg.modelspace().add_blockref(entity_type, (0, 0))
    dwg.saveas(f"./output_dxf/{entity_type}.dxf")


def read_prototype_dxf(directory):
    dxf_files = dxfblocks.DxfBlocks(directory)
    dxf_dwgs = dxf_files.get_dwgs()
    for dwg in dxf_dwgs:
        dxf_to_data.write_blocks(dwg)


if __name__ == '__main__':
    # DXFGenerator().cmdloop()
    # create_tc_test1()
    create_tc_test2()
    # block_import_test()
    # block_output_test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# 规则
# class name        PascalCase
# module/file name  snake_case
# function          snake_case
# 私有变量            snake_case
# 函数参数            snake_case
