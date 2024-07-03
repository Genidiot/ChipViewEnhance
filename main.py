from src.Parser import ParserEntity
from src.Parser import ParserLayout
from src.Draw import DrawChipView
from src.Parser import ParserSWH
from src.Draw import DrawSWH
from src.Draw import DrawLine


def create_tc():
    config_chip_view = ParserLayout.ChipViewLayout(f"./config/chipview.json")
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

    normal_line = DrawLine.NormalLineCreate(swh_l_config, swh_l, dwg_chip_view)
    normal_line.create_line()
    line_l = normal_line.get_line_l_list()
    line_r = normal_line.get_line_r_list()
    print(line_r)

    chip_view.add_tile_refs()
    chip_view.add_segment(pins, line_r, line_l)
    chip_view.save_sa(f"./result_dxf/test2.dxf")


if __name__ == '__main__':
    create_tc()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# 规则
# class name        PascalCase
# module/file name  snake_case
# function          snake_case
# 私有变量            snake_case
# 函数参数            snake_case
