import json
from typing import List
from src.DataBase.point import PointF
from src.DataBase.graphic import chip_view_graphic


class LogicRegion:
    def __init__(self, point_start: PointF, point_end: PointF, item_width=10, item_height=10):
        self.point_start = point_start
        self.point_end = point_end
        self.item_width = item_width
        self.item_height = item_height

    def set_point_start(self, point_start: PointF):
        self.point_start = point_start

    def set_point_end(self, point_end: PointF):
        self.point_end = point_end

    def __min_row(self):
        return min(self.point_start.get_row(), self.point_end.get_row())

    def __min_column(self):
        return min(self.point_start.get_column(), self.point_end.get_column())

    def __max_row(self):
        return max(self.point_start.get_row(), self.point_end.get_row())

    def __max_column(self):
        return max(self.point_start.get_column(), self.point_end.get_column())

    def is_row_in_region(self, row):
        if self.__min_row() <= row <= self.__max_row():
            return True
        else:
            return False

    def is_column_in_region(self, column):
        if self.__min_column() <= column <= self.__max_column():
            return True
        else:
            return False

    def is_column_in_region2(self, column):
        if self.__min_column() <= column < self.__max_column():
            return True
        else:
            return False

    def is_column_in_region3(self, column):
        if self.__min_column() < column <= self.__max_column():
            return True
        else:
            return False

    def get_logic_points(self) -> list:
        point_list = []
        row = self.__min_row()
        while row < self.__max_row() + 1:
            column = self.__min_column()
            while column < self.__max_column() + 1:
                point_list.append(PointF(column, row))
                column += self.item_width
            row += self.item_height
        return point_list


class ItemRegions:
    def __init__(self, item_type="", item_width=10, item_height=10):
        self.item_type = item_type
        self.item_width = item_width
        self.item_height = item_height
        self.regions: List[LogicRegion] = []

    def add_region(self, region: LogicRegion):
        self.regions.append(region)

    def set_regions(self, region_list: list):
        self.regions = region_list

    def get_regions(self):
        return self.regions

    def set_item_type(self, item_type: str):
        self.item_type = item_type

    def get_item_type(self):
        return self.item_type

    def set_item_width(self, item_width):
        self.item_width = item_width

    def get_item_width(self):
        return self.item_width

    def set_item_height(self, item_height):
        self.item_height = item_height

    def get_item_height(self):
        return self.item_height


class ChipViewLayout:
    def __init__(self, filename):
        self.filename = filename
        self.name = ""
        self.row_count = 0
        self.column_count = 0
        self.row_heights = {}
        self.column_widths = {}
        self.items_region: List[ItemRegions] = list()

        self.__read_config()
        self.add_to_graphic()

    def __read_config(self):
        with open(self.filename, 'r') as configfile:
            configuration = json.load(configfile)
        self.__parser_config(configuration)

    def __parser_config(self, configuration: dict):
        self.name = configuration["deviceName"]
        self.row_count = configuration["rowNum"]
        self.column_count = configuration["colNum"]
        self.row_heights = {int(key) if key.isdigit() else key: value for key, value in configuration["rowHeights"].items()}
        self.column_widths = {int(key) if key.isdigit() else key: value for key, value in configuration["columnWidths"].items()}

        for item_region in configuration["itemRegion"]:
            temp_item_region = ItemRegions(item_region["type"], item_region["width"], item_region["height"])
            for region in item_region["regions"]:
                point_start = PointF(region["startX"], region["startY"])
                point_end = PointF(region["endX"], region["endY"])
                temp_item_region.add_region(
                    LogicRegion(point_start, point_end, item_region["width"], item_region["height"]))
            self.items_region.append(temp_item_region)

    def get_config_name(self):
        return self.name

    def get_row_count(self):
        return self.row_count

    def get_column_count(self):
        return self.column_count

    def get_items_region(self):
        return self.items_region

    def get_type_names(self):
        typenames = list()
        for items_region in self.items_region:
            typenames.append(items_region.get_item_type())
        return typenames

    def add_to_graphic(self):
        chip_view_graphic.set_device_name(device_name=self.name)
        chip_view_graphic.set_row_count(row_count=self.row_count)
        chip_view_graphic.set_column_count(column_count=self.column_count)
        chip_view_graphic.set_max_row_index(max_row_index=self.row_count - 1)
        chip_view_graphic.set_max_column_index(max_column_index=self.column_count - 1)

        for key, value in self.row_heights.items():
            chip_view_graphic.set_row_height(row=key, height=value)
        for key, value in self.column_widths.items():
            chip_view_graphic.set_col_width(col=key, width=value)
        chip_view_graphic.update_mappings()

        for item_regions in self.items_region:
            for region in item_regions.get_regions():
                for point in region.get_logic_points():
                    column = int(point.get_column())
                    row = int(point.get_row())
                    insert_point = chip_view_graphic.logic_to_physical[(column, row)]
                    ref_name = item_regions.get_item_type()
                    self.extract_swh(ref_name, column, row)
                    chip_view_graphic.add_new_entity_inst(entity_type=ref_name,
                                                          ref_entity_name=ref_name,
                                                          position_=insert_point,
                                                          logic_x=column,
                                                          logic_y=row,
                                                          id_=None)
        print(chip_view_graphic.row_heights)
        print(chip_view_graphic.column_widths)
        print(chip_view_graphic.render_layout())
        print(chip_view_graphic.swh_point_map)

    @staticmethod
    def extract_swh(ref_name, column, row):
        if ref_name != "SWHL" and ref_name != "SWHR":
            return
        chip_view_graphic.add_swh_point((column, row))
