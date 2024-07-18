from src.DataBase.graphic import chip_view_graphic


def modify_graphic():
    chip_view_graphic.insert_row(2, 3000)
    chip_view_graphic.insert_column(4, 3000)
    chip_view_graphic.update_mappings()
    print(chip_view_graphic.row_heights)
    print(chip_view_graphic.column_widths)
    print(chip_view_graphic.render_layout())
