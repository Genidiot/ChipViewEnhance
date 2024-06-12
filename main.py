from src.Parser import ParserEntity
from src.Parser import ParserLayout
from src.Draw import DrawChipView


def create_tc():
    config_chip_view = ParserLayout.ChipViewLayout(f"./config/chipview.json")
    ParserEntity.EntityParser(f"./config/SWHL.json")
    ParserEntity.EntityParser(f"./config/CLCL.json")
    chip_view = DrawChipView.DxfChipView(config_chip_view)
    chip_view.add_tile_refs()
    chip_view.save_sa(f"./result_dxf/test.dxf")


if __name__ == '__main__':
    create_tc()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
