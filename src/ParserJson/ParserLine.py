import json
from src.ParserJson.ParserSWH import SwhConfig
from src.ParserJson.ParserSWH import Layout
from src.ParserJson.ParserSWH import MuxNames
from src.DataBase.graphic import chip_view_graphic
from src.DataBase.point import PointF
from src.DataBase.item import PolygonLineItem
from src.DataBase.entity import Entity
from src.DataBase import entity_lib
from src.Draw import calculate_line
import re


def get_group(group_name: str):
    if group_name.find("L1BEG") != -1:
        return 1
    elif group_name.find("L2BEG") != -1:
        return 2
    elif group_name.find("L4BEG") != -1:
        return 4
    elif group_name.find("L6BEG") != -1:
        return 6
    elif group_name.find("L12BEG") != -1:
        return 12
    else:
        return -1


def extract_number(input_string):
    pattern = r'\[(\d+)\]'
    match = re.search(pattern, input_string)
    if match:
        return int(match.group(1))
    else:
        return None


def get_ee_pin_to_edge(swh_config, pin_name, edge):
    beg_insert_point = swh_config.get_pin_point(pin_name)
    beg_pin_distance = int(edge - beg_insert_point[0])
    end_name = pin_name.replace("beg", "end").replace("BEG", "END")
    end_insert_point = swh_config.get_pin_point(end_name)
    end_pin_distance = int(end_insert_point[0])
    return beg_pin_distance, end_pin_distance, end_name


def get_ww_pin_to_edge(swh_config, pin_name, edge):
    beg_insert_point = swh_config.get_pin_point(pin_name)
    beg_pin_distance = int(beg_insert_point[0])
    end_name = pin_name.replace("beg", "end").replace("BEG", "END")
    end_insert_point = swh_config.get_pin_point(end_name)
    end_pin_distance = int(edge - end_insert_point[0])
    return beg_pin_distance, end_pin_distance, end_name


def get_nn_pin_to_edge(swh_config, pin_name, edge):
    beg_insert_point = swh_config.get_pin_point(pin_name)
    beg_pin_distance = int(edge - beg_insert_point[1])
    end_name = pin_name.replace("beg", "end").replace("BEG", "END")
    end_insert_point = swh_config.get_pin_point(end_name)
    end_pin_distance = int(end_insert_point[1])
    return beg_pin_distance, end_pin_distance, end_name


def get_ss_pin_to_edge(swh_config, pin_name, edge):
    beg_insert_point = swh_config.get_pin_point(pin_name)
    beg_pin_distance = int(beg_insert_point[1])
    end_name = pin_name.replace("beg", "end").replace("BEG", "END")
    end_insert_point = swh_config.get_pin_point(end_name)
    end_pin_distance = int(edge - end_insert_point[1])
    return beg_pin_distance, end_pin_distance, end_name


def create_polygon_line(points_list):
    polygon_line_item = PolygonLineItem()
    for point in points_list:
        polygon_line_item.add_point(point)
    return polygon_line_item


class LineConfig:
    def __init__(self, filename):
        self.filename = filename
        self.gap = 0
        self.min_y = 0
        self.max_y = 0
        self.min_x = 0
        self.max_x = 0
        self.space = 0
        self.multi = 0

        self.__read_config()

    def __read_config(self):
        with open(self.filename, 'r') as configfile:
            configuration = json.load(configfile)
        self.__parser_config(configuration)

    def __parser_config(self, configuration: dict):
        self.gap = configuration["line_gap"]
        self.min_y = configuration["min_y"]
        self.max_y = configuration["max_y"]
        self.min_x = configuration["min_x"]
        self.max_x = configuration["max_x"]
        self.space = configuration["tile_space"]
        self.multi = configuration["multiple"]

    def create_line_entity(self, swh_config):
        units, grid = calculate_line.process_units()
        each_row_distances, each_col_distances = calculate_line.calculate_distances(grid)

        unique_row_logical_distances = calculate_line.unique_distances(each_row_distances)
        unique_col_logical_distances = calculate_line.unique_distances(each_col_distances)

        self.create_ew_line_points(swh_config, unique_row_logical_distances)
        self.create_ns_line_points(swh_config, unique_col_logical_distances)

    def create_ew_line_points(self, swh_config: SwhConfig, logical_distances):
        for section in swh_config.down_layout:
            section: Layout
            if section.get_index() != 9:
                continue
            for Mux in section.mux_group_list:
                Mux: MuxNames
                line_length = get_group(Mux.group_name)
                if line_length == -1:
                    continue
                length_combinations = logical_distances.get(line_length)
                if length_combinations is None:
                    continue
                line_group_num = len(Mux.mux_name)
                drop_height = line_group_num
                stair_num = line_length
                drop_num = line_length - 1
                point_num = line_length * 2 + 2
                line_group_start_y = self.min_y - self.gap
                width = swh_config.get_width()

                for index, combination in enumerate(length_combinations):
                    chip_view_graphic.normalLine_e_map[combination] = []
                    single_line_start_y = line_group_start_y
                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [PointF(0, 0)]

                        x = 0
                        y = single_line_start_y
                        beg_to_edge, edge_to_end, end_name = get_ee_pin_to_edge(swh_config, pin_name, width)

                        for i in range(stair_num):
                            count = count + 1
                            x = x
                            y = single_line_start_y - drop_height * i
                            point_list.append(PointF(x, y))

                            count = count + 1
                            if count == point_num - 1:
                                x = beg_to_edge + (sum(combination) - 1) * (width + self.space) \
                                    + self.space + edge_to_end
                            else:
                                x = beg_to_edge + (sum(combination[:i + 1]) - 1) * (width + self.space) + self.space \
                                    + width / 2 - self.multi * line_group_num * i - self.multi * pin_index

                            y = y
                            point_list.append(PointF(x, y))
                        point_list.append(PointF(x, 0))
                        single_line_start_y = single_line_start_y - self.gap
                        self.min_y = y

                        block_name = pin_name + "-" + end_name + "-" + str(index)
                        chip_view_graphic.normalLine_e_map[combination].append(block_name)

                        entity = Entity(entity_name=block_name)
                        entity.add_item(create_polygon_line(point_list))
                        entity_library = entity_lib.entity_lib
                        entity_library.add_entity(block_name, entity)

        for section in swh_config.up_layout:
            if section.get_index() != 0:
                continue
            for Mux in section.mux_group_list:
                line_length = get_group(Mux.group_name)
                if line_length == -1:
                    continue
                length_combinations = logical_distances.get(line_length)
                if length_combinations is None:
                    continue
                line_group_num = len(Mux.mux_name)
                rise_height = line_group_num
                stair_num = line_length
                rise_num = line_length - 1
                point_num = line_length * 2 + 2
                line_group_start_y = self.max_y + self.gap
                width = swh_config.get_width()

                for index, combination in enumerate(length_combinations):
                    chip_view_graphic.normalLine_w_map[combination] = []
                    single_line_start_y = line_group_start_y
                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [PointF(0, 0)]

                        x = 0
                        y = single_line_start_y
                        beg_to_edge, edge_to_end, end_name = get_ww_pin_to_edge(swh_config, pin_name, width)

                        for i in range(stair_num):
                            count = count + 1
                            x = x
                            y = single_line_start_y + rise_height * i
                            point_list.append(PointF(x, y))

                            count = count + 1
                            if count == point_num - 1:
                                x = 0 - (beg_to_edge + (sum(combination) - 1) * (width + self.space)
                                         + self.space + edge_to_end)
                            else:
                                x = 0 - (beg_to_edge + (sum(combination[:i+1]) - 1) * (width + self.space) + self.space
                                         + width / 2 - self.multi * line_group_num * i - self.multi * pin_index)

                            y = y
                            point_list.append(PointF(x, y))
                        point_list.append(PointF(x, 0))
                        single_line_start_y = single_line_start_y + self.gap
                        self.max_y = y

                        block_name = pin_name + "-" + end_name + "-" + str(index)
                        chip_view_graphic.normalLine_w_map[combination].append(block_name)

                        entity = Entity(entity_name=block_name)
                        entity.add_item(create_polygon_line(point_list))
                        entity_library = entity_lib.entity_lib
                        entity_library.add_entity(block_name, entity)

    def create_ns_line_points(self, swh_config: SwhConfig, logic_distances):
        for section in swh_config.left_layout:
            section: Layout
            if section.get_index() != 9:
                continue
            for Mux in section.mux_group_list:
                Mux: MuxNames
                line_length = get_group(Mux.group_name)
                if line_length == -1:
                    continue
                length_combinations = logic_distances.get(line_length)
                if length_combinations is None:
                    continue
                line_group_num = len(Mux.mux_name)
                ext_width = line_group_num
                stair_num = line_length
                ext_num = line_length - 1
                point_num = line_length * 2 + 2
                line_group_start_x = self.min_x - self.gap
                height = swh_config.get_height()

                for index, combination in enumerate(length_combinations):
                    chip_view_graphic.normalLine_n_map[combination] = []
                    single_line_start_x = line_group_start_x
                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [PointF(0, 0)]

                        x = single_line_start_x
                        y = 0
                        beg_to_edge, edge_to_end, end_name = get_nn_pin_to_edge(swh_config, pin_name, height)

                        for i in range(stair_num):
                            count = count + 1
                            x = single_line_start_x - ext_width * i
                            y = y
                            point_list.append(PointF(x, y))

                            count = count + 1
                            if count == point_num - 1:
                                y = beg_to_edge + (sum(combination) - 1) * (height + self.space) \
                                    + self.space + edge_to_end
                            else:
                                y = beg_to_edge + (sum(combination[:i+1]) - 1) * (height + self.space) + self.space \
                                    + height / 2 - self.multi * line_group_num * i - self.multi * pin_index

                            x = x
                            point_list.append(PointF(x, y))
                        point_list.append(PointF(0, y))
                        single_line_start_x = single_line_start_x - self.gap
                        self.min_x = x

                        block_name = pin_name + "-" + end_name + "-" + str(index)
                        chip_view_graphic.normalLine_n_map[combination].append(block_name)

                        entity = Entity(entity_name=block_name)
                        entity.add_item(create_polygon_line(point_list))
                        entity_library = entity_lib.entity_lib
                        entity_library.add_entity(block_name, entity)

        for section in swh_config.right_layout:
            section: Layout
            if section.get_index() != 0:
                continue
            for Mux in section.mux_group_list:
                Mux: MuxNames
                line_length = get_group(Mux.group_name)
                if line_length == -1:
                    continue
                length_combinations = logic_distances.get(line_length)
                if length_combinations is None:
                    continue
                line_group_num = len(Mux.mux_name)
                ext_width = line_group_num
                stair_num = line_length
                ext_num = line_length - 1
                point_num = line_length * 2 + 2
                line_group_start_x = self.max_x + self.gap
                height = swh_config.get_height()

                for index, combination in enumerate(length_combinations):
                    chip_view_graphic.normalLine_s_map[combination] = []
                    single_line_start_x = line_group_start_x
                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [PointF(0, 0)]

                        x = single_line_start_x
                        y = 0
                        beg_to_edge, edge_to_end, end_name = get_ss_pin_to_edge(swh_config, pin_name, height)

                        for i in range(stair_num):
                            count = count + 1
                            x = single_line_start_x + ext_width * i
                            y = y
                            point_list.append(PointF(x, y))

                            count = count + 1
                            if count == point_num - 1:
                                y = 0 - (beg_to_edge + (sum(combination) - 1) * (height + self.space)
                                         + self.space + edge_to_end)
                            else:
                                y = 0 - (beg_to_edge + (sum(combination[:i+1]) - 1) * (height + self.space) + self.space
                                         + height / 2 - self.multi * line_group_num * i - self.multi * pin_index)

                            x = x
                            point_list.append(PointF(x, y))
                        point_list.append(PointF(0, y))
                        single_line_start_x = single_line_start_x + self.gap
                        self.max_x = x

                        block_name = pin_name + "-" + end_name + "-" + str(index)
                        chip_view_graphic.normalLine_s_map[combination].append(block_name)

                        entity = Entity(entity_name=block_name)
                        entity.add_item(create_polygon_line(point_list))
                        entity_library = entity_lib.entity_lib
                        entity_library.add_entity(block_name, entity)
