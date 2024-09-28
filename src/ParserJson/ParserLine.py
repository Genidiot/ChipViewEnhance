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


def get_edge_line_pin_to_edge(swh_config, pin_name, edge, direction):
    beg_insert_point = swh_config.get_pin_point(pin_name)
    if pin_name.startswith("EE"):
        name = pin_name.replace("EE", "WW")
    elif pin_name.startswith("WW"):
        name = pin_name.replace("WW", "EE")
    elif pin_name.startswith("NN"):
        name = pin_name.replace("NN", "SS")
    elif pin_name.startswith("SS"):
        name = pin_name.replace("SS", "NN")
    end_name = name.replace("beg", "end").replace("BEG", "END")
    end_insert_point = swh_config.get_pin_point(end_name)

    if direction == 'EE_edge':
        beg_pin_distance = int(edge - beg_insert_point[0])
        end_pin_distance = int(edge - end_insert_point[0])
    elif direction == 'WW_edge':
        beg_pin_distance = int(beg_insert_point[0])
        end_pin_distance = int(end_insert_point[0])
    elif direction == 'NN_edge':
        beg_pin_distance = int(edge - beg_insert_point[1])
        end_pin_distance = int(edge - end_insert_point[1])
    elif direction == 'SS_edge':
        beg_pin_distance = int(beg_insert_point[1])
        end_pin_distance = int(end_insert_point[1])
    else:
        raise ValueError("Invalid direction")

    return beg_pin_distance, end_pin_distance, end_name


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
        # print(units)
        # print(grid)

        unique_row_logical_distances = calculate_line.unique_distances(each_row_distances)
        unique_col_logical_distances = calculate_line.unique_distances(each_col_distances)

        # print(unique_row_logical_distances)
        # print(unique_col_logical_distances)

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
                    if 0 in combination:
                        self.create_e_edge_line(Mux, line_length, swh_config, combination, line_group_start_y, index)
                        continue
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
                    if 0 in combination:
                        self.create_w_edge_line(Mux, line_length, swh_config, combination, line_group_start_y, index)
                        continue
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
                    if 0 in combination:
                        self.create_n_edge_line(Mux, line_length, swh_config, combination, line_group_start_x, index)
                        continue
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
                    if 0 in combination:
                        self.create_s_edge_line(Mux, line_length, swh_config, combination, line_group_start_x, index)
                        continue
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

    def create_e_edge_line(self, mux, line_length, swh_config, combination, line_group_start_y, index):
        line_group_num = len(mux.mux_name)
        drop_height = line_group_num
        new_point_num = line_length * 2 + 4
        single_line_start_y = line_group_start_y
        width = swh_config.get_width()
        height = swh_config.get_height()

        for pin_name in mux.mux_name:
            pin_index = extract_number(pin_name)
            count = 1
            point_list = [PointF(0, 0)]

            x = 0
            y = single_line_start_y
            beg_to_edge, edge_to_end, end_name = get_edge_line_pin_to_edge(swh_config, pin_name, width, "EE_edge")

            for i, length in enumerate(combination):

                if length > 0:
                    count = count + 1
                    x = x
                    y = single_line_start_y - drop_height * i
                    point_list.append(PointF(x, y))

                    count = count + 1
                    if i == 0:
                        x = x + beg_to_edge + (length - 1) * (width + self.space) + self.space \
                            + width / 2 - self.multi * line_group_num * i - self.multi * pin_index
                    else:
                        x = x + self.multi * line_group_num * (i-1) + width / 2 + (length - 1) * (width + self.space) \
                            + self.space + width / 2 - self.multi * line_group_num * i

                    y = y
                    point_list.append(PointF(x, y))

                elif length == 0:
                    count = count + 1
                    x = x
                    y = single_line_start_y - drop_height * i
                    point_list.append(PointF(x, y))

                    if i == 0:
                        count = count + 1
                        x = x + beg_to_edge + 200 + 50 * line_length + self.multi * pin_index
                        y = y
                        point_list.append(PointF(x, y))

                        count = count + 1
                        x = x
                        y = height - y
                        point_list.append(PointF(x, y))

                        count = count + 1
                        if count == new_point_num - 1:
                            x = x - 200 - 50 * line_length - self.multi * pin_index - edge_to_end
                            y = y
                            point_list.append(PointF(x, y))
                        else:
                            x = x - 200 - 50 * line_length - self.multi * pin_index - width / 2\
                                + self.multi * line_group_num * i + self.multi * pin_index
                            y = y
                            point_list.append(PointF(x, y))
                    else:
                        count = count + 1
                        x = x + self.multi * line_group_num * (i-1) + self.multi * pin_index + width / 2\
                            + 200 + 50 * line_length + self.multi * pin_index + self.multi * line_group_num * i
                        y = y
                        point_list.append(PointF(x, y))

                        count = count + 1
                        x = x
                        y = height - y
                        point_list.append(PointF(x, y))

                        count = count + 1
                        if count == new_point_num - 1:
                            x = x - 200 - 50 * line_length - self.multi * pin_index - edge_to_end\
                                - self.multi * line_group_num * i
                            y = y
                            point_list.append(PointF(x, y))
                        else:
                            x = x - 200 - 50 * line_length - self.multi * pin_index - self.multi * line_group_num * i\
                                - width / 2 + self.multi * line_group_num * i + self.multi * pin_index
                            y = y
                            point_list.append(PointF(x, y))

                elif length < 0:
                    count = count + 1
                    x = x
                    y = y + drop_height
                    point_list.append(PointF(x, y))

                    count = count + 1
                    if count == new_point_num - 1:
                        x = x - self.multi * line_group_num * (i - 1) - self.multi * pin_index\
                            - width / 2 - (abs(length) - 1) * (width + self.space) - self.space - edge_to_end
                        y = y
                        point_list.append(PointF(x, y))
                    else:
                        x = x - self.multi * line_group_num * (i - 1) - width / 2 - (abs(length) - 1) * (
                                    width + self.space) - self.space - width / 2 + self.multi * line_group_num * i
                        y = y
                        point_list.append(PointF(x, y))

            point_list.append(PointF(x, height))
            single_line_start_y = single_line_start_y - self.gap

            block_name = pin_name + "-" + end_name + "-" + str(index)
            chip_view_graphic.normalLine_e_map[combination].append(block_name)

            entity = Entity(entity_name=block_name)
            entity.add_item(create_polygon_line(point_list))
            entity_library = entity_lib.entity_lib
            entity_library.add_entity(block_name, entity)

    def create_w_edge_line(self, mux, line_length, swh_config, combination, line_group_start_y, index):
        line_group_num = len(mux.mux_name)
        drop_height = line_group_num
        new_point_num = line_length * 2 + 4
        single_line_start_y = line_group_start_y
        width = swh_config.get_width()
        height = swh_config.get_height()

        for pin_name in mux.mux_name:
            pin_index = extract_number(pin_name)
            count = 1
            point_list = [PointF(0, 0)]

            x = 0
            y = single_line_start_y
            beg_to_edge, edge_to_end, end_name = get_edge_line_pin_to_edge(swh_config, pin_name, width, "WW_edge")

            for i, length in enumerate(combination):

                if length > 0:
                    count = count + 1
                    x = x
                    y = single_line_start_y + drop_height * i
                    point_list.append(PointF(x, y))

                    count = count + 1
                    if i == 0:
                        x = x - (beg_to_edge + (length - 1) * (width + self.space) + self.space
                                 + width / 2 - self.multi * line_group_num * i - self.multi * pin_index)
                    else:
                        x = x - (self.multi * line_group_num * (i - 1) + width / 2 + (length - 1) * (width + self.space)
                                 + self.space + width / 2 - self.multi * line_group_num * i)

                    y = y
                    point_list.append(PointF(x, y))

                elif length == 0:
                    count = count + 1
                    x = x
                    y = single_line_start_y + drop_height * i
                    point_list.append(PointF(x, y))

                    if i == 0:
                        count = count + 1
                        x = x - (beg_to_edge + 200 + 50 * line_length + self.multi * pin_index)
                        y = y
                        point_list.append(PointF(x, y))

                        count = count + 1
                        x = x
                        y = -y - height
                        point_list.append(PointF(x, y))

                        count = count + 1
                        if count == new_point_num - 1:
                            x = x - (- 200 - 50 * line_length - self.multi * pin_index - edge_to_end)
                            y = y
                            point_list.append(PointF(x, y))
                        else:
                            x = x - (- 200 - 50 * line_length - self.multi * pin_index - width / 2
                                     + self.multi * line_group_num * i + self.multi * pin_index)
                            y = y
                            point_list.append(PointF(x, y))
                    else:
                        count = count + 1
                        x = x - (self.multi * line_group_num * (i - 1) + self.multi * pin_index + width / 2
                                 + 200 + 50 * line_length + self.multi * pin_index + self.multi * line_group_num * i)
                        y = y
                        point_list.append(PointF(x, y))

                        count = count + 1
                        x = x
                        y = -y - height
                        point_list.append(PointF(x, y))

                        count = count + 1
                        if count == new_point_num - 1:
                            x = x - (- 200 - 50 * line_length - self.multi * pin_index - edge_to_end
                                     - self.multi * line_group_num * i)
                            y = y
                            point_list.append(PointF(x, y))
                        else:
                            x = x - (- 200 - 50 * line_length - self.multi * pin_index - self.multi * line_group_num * i
                                     - width / 2 + self.multi * line_group_num * i + self.multi * pin_index)
                            y = y
                            point_list.append(PointF(x, y))

                elif length < 0:
                    count = count + 1
                    x = x
                    y = y - drop_height
                    point_list.append(PointF(x, y))

                    count = count + 1
                    if count == new_point_num - 1:
                        x = x - (- self.multi * line_group_num * (i - 1) - self.multi * pin_index
                                 - width / 2 - (abs(length) - 1) * (width + self.space) - self.space - edge_to_end)
                        y = y
                        point_list.append(PointF(x, y))
                    else:
                        x = x - (- self.multi * line_group_num * (i - 1) - width / 2 - (abs(length) - 1) * (
                                width + self.space) - self.space - width / 2 + self.multi * line_group_num * i)
                        y = y
                        point_list.append(PointF(x, y))

            point_list.append(PointF(x, -height))
            single_line_start_y = single_line_start_y + self.gap

            block_name = pin_name + "-" + end_name + "-" + str(index)
            chip_view_graphic.normalLine_w_map[combination].append(block_name)

            entity = Entity(entity_name=block_name)
            entity.add_item(create_polygon_line(point_list))
            entity_library = entity_lib.entity_lib
            entity_library.add_entity(block_name, entity)

    def create_n_edge_line(self, mux, line_length, swh_config, combination, line_group_start_x, index):
        line_group_num = len(mux.mux_name)
        drop_height = line_group_num
        new_point_num = line_length * 2 + 4
        single_line_start_x = line_group_start_x
        width = swh_config.get_width()
        height = swh_config.get_height()

        for pin_name in mux.mux_name:
            pin_index = extract_number(pin_name)
            count = 1
            point_list = [PointF(0, 0)]

            x = single_line_start_x
            y = 0
            beg_to_edge, edge_to_end, end_name = get_edge_line_pin_to_edge(swh_config, pin_name, width, "NN_edge")

            for i, length in enumerate(combination):

                if length > 0:
                    count = count + 1
                    x = single_line_start_x - drop_height * i
                    y = y
                    point_list.append(PointF(x, y))

                    count = count + 1
                    if i == 0:
                        y = y + beg_to_edge + (length - 1) * (height + self.space) + self.space \
                            + height / 2 - self.multi * line_group_num * i - self.multi * pin_index
                    else:
                        y = y + self.multi * line_group_num * (i - 1) + height / 2 + self.space \
                            + (length - 1) * (height + self.space) + height / 2 - self.multi * line_group_num * i

                    x = x
                    point_list.append(PointF(x, y))

                elif length == 0:
                    count = count + 1
                    x = single_line_start_x - drop_height * i
                    y = y
                    point_list.append(PointF(x, y))

                    if i == 0:
                        count = count + 1
                        y = y + beg_to_edge + 200 + 50 * line_length + self.multi * pin_index
                        x = x
                        point_list.append(PointF(x, y))

                        count = count + 1
                        y = y
                        x = width - x
                        point_list.append(PointF(x, y))

                        count = count + 1
                        if count == new_point_num - 1:
                            y = y - 200 - 50 * line_length - self.multi * pin_index - edge_to_end
                            x = x
                            point_list.append(PointF(x, y))
                        else:
                            y = y - 200 - 50 * line_length - self.multi * pin_index - height / 2 \
                                + self.multi * line_group_num * i + self.multi * pin_index
                            x = x
                            point_list.append(PointF(x, y))
                    else:
                        count = count + 1
                        y = y + self.multi * line_group_num * (i - 1) + self.multi * pin_index + height / 2 \
                            + 200 + 50 * line_length + self.multi * pin_index + self.multi * line_group_num * i
                        x = x
                        point_list.append(PointF(x, y))

                        count = count + 1
                        y = y
                        x = width - x
                        point_list.append(PointF(x, y))

                        count = count + 1
                        if count == new_point_num - 1:
                            y = y - 200 - 50 * line_length - self.multi * pin_index - edge_to_end \
                                - self.multi * line_group_num * i
                            x = x
                            point_list.append(PointF(x, y))
                        else:
                            y = y - 200 - 50 * line_length - self.multi * pin_index - self.multi * line_group_num * i \
                                - height / 2 + self.multi * line_group_num * i + self.multi * pin_index
                            x = x
                            point_list.append(PointF(x, y))

                elif length < 0:
                    count = count + 1
                    x = x + drop_height
                    y = y
                    point_list.append(PointF(x, y))

                    count = count + 1
                    if count == new_point_num - 1:
                        y = y - self.multi * line_group_num * (i - 1) - self.multi * pin_index \
                            - height / 2 - (abs(length) - 1) * (height + self.space) - self.space - edge_to_end
                        x = x
                        point_list.append(PointF(x, y))
                    else:
                        y = y - self.multi * line_group_num * (i - 1) - height / 2 - (abs(length) - 1) * (
                                height + self.space) - self.space - height / 2 + self.multi * line_group_num * i
                        x = x
                        point_list.append(PointF(x, y))

            point_list.append(PointF(width, y))
            single_line_start_x = single_line_start_x - self.gap

            block_name = pin_name + "-" + end_name + "-" + str(index)
            chip_view_graphic.normalLine_n_map[combination].append(block_name)

            entity = Entity(entity_name=block_name)
            entity.add_item(create_polygon_line(point_list))
            entity_library = entity_lib.entity_lib
            entity_library.add_entity(block_name, entity)

    def create_s_edge_line(self, mux, line_length, swh_config, combination, line_group_start_x, index):
        line_group_num = len(mux.mux_name)
        drop_height = line_group_num
        new_point_num = line_length * 2 + 4
        single_line_start_x = line_group_start_x
        width = swh_config.get_width()
        height = swh_config.get_height()

        for pin_name in mux.mux_name:
            pin_index = extract_number(pin_name)
            count = 1
            point_list = [PointF(0, 0)]

            x = single_line_start_x
            y = 0
            beg_to_edge, edge_to_end, end_name = get_edge_line_pin_to_edge(swh_config, pin_name, width, "SS_edge")

            for i, length in enumerate(combination):

                if length > 0:
                    count = count + 1
                    x = single_line_start_x + drop_height * i
                    y = y
                    point_list.append(PointF(x, y))

                    count = count + 1
                    if i == 0:
                        y = y - (beg_to_edge + (length - 1) * (height + self.space) + self.space
                                 + height / 2 - self.multi * line_group_num * i - self.multi * pin_index)
                    else:
                        y = y - (self.multi * line_group_num * (i - 1) + height / 2 + self.space
                                 + (length - 1) * (height + self.space) + height / 2 - self.multi * line_group_num * i)

                    x = x
                    point_list.append(PointF(x, y))

                elif length == 0:
                    count = count + 1
                    x = single_line_start_x + drop_height * i
                    y = y
                    point_list.append(PointF(x, y))

                    if i == 0:
                        count = count + 1
                        y = y - (beg_to_edge + 200 + 50 * line_length + self.multi * pin_index)
                        x = x
                        point_list.append(PointF(x, y))

                        count = count + 1
                        y = y
                        x = -x - width
                        point_list.append(PointF(x, y))

                        count = count + 1
                        if count == new_point_num - 1:
                            y = y - (- 200 - 50 * line_length - self.multi * pin_index - edge_to_end)
                            x = x
                            point_list.append(PointF(x, y))
                        else:
                            y = y - (- 200 - 50 * line_length - self.multi * pin_index - height / 2
                                     + self.multi * line_group_num * i + self.multi * pin_index)
                            x = x
                            point_list.append(PointF(x, y))
                    else:
                        count = count + 1
                        y = y - (self.multi * line_group_num * (i - 1) + self.multi * pin_index + height / 2
                                 + 200 + 50 * line_length + self.multi * pin_index + self.multi * line_group_num * i)
                        x = x
                        point_list.append(PointF(x, y))

                        count = count + 1
                        y = y
                        x = -x - width
                        point_list.append(PointF(x, y))

                        count = count + 1
                        if count == new_point_num - 1:
                            y = y - (- 200 - 50 * line_length - self.multi * pin_index - edge_to_end
                                     - self.multi * line_group_num * i)
                            x = x
                            point_list.append(PointF(x, y))
                        else:
                            y = y - (- 200 - 50 * line_length - self.multi * pin_index - self.multi * line_group_num * i
                                     - height / 2 + self.multi * line_group_num * i + self.multi * pin_index)
                            x = x
                            point_list.append(PointF(x, y))

                elif length < 0:
                    count = count + 1
                    x = x - drop_height
                    y = y
                    point_list.append(PointF(x, y))

                    count = count + 1
                    if count == new_point_num - 1:
                        y = y - (- self.multi * line_group_num * (i - 1) - self.multi * pin_index
                                 - height / 2 - (abs(length) - 1) * (height + self.space) - self.space - edge_to_end)
                        x = x
                        point_list.append(PointF(x, y))
                    else:
                        y = y - (- self.multi * line_group_num * (i - 1) - height / 2 - (abs(length) - 1) * (
                                height + self.space) - self.space - height / 2 + self.multi * line_group_num * i)
                        x = x
                        point_list.append(PointF(x, y))

            point_list.append(PointF(-width, y))
            single_line_start_x = single_line_start_x + self.gap

            block_name = pin_name + "-" + end_name + "-" + str(index)
            chip_view_graphic.normalLine_s_map[combination].append(block_name)

            entity = Entity(entity_name=block_name)
            entity.add_item(create_polygon_line(point_list))
            entity_library = entity_lib.entity_lib
            entity_library.add_entity(block_name, entity)
