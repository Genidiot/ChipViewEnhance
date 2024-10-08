from src.ParserJson import ParserSWH
from src.ParserJson.ParserSWH import Layout
from src.ParserJson.ParserSWH import MuxNames
from src.Draw import DrawSWH
from src.DataBase.graphic import chip_view_graphic
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


class NormalLineCreate:
    def __init__(self, config: ParserSWH.SwhConfig, swh: DrawSWH.SwhCreate, dwg, space):
        self.dwg = dwg
        self.msp = self.dwg.modelspace()
        self.config = config
        self.swh = swh

        # self.drop_height = 0
        # self.drop_num = 0
        self.gap = 1
        self.min_y = -99
        self.max_y = 99
        self.min_x = -99
        self.max_x = 99
        self.space = space
        self.multi = 4
        self.line_r_list = list()
        self.line_l_list = list()

    def get_line_r_list(self):
        return self.line_r_list

    def get_line_l_list(self):
        return self.line_l_list

    def get_ee_pin_to_edge(self, pin_name, edge):
        beg_insert_point = self.swh.get_pin_point(pin_name)
        beg_pin_distance = int(edge - beg_insert_point[0])
        end_name = pin_name.replace("beg", "end").replace("BEG", "END")
        end_insert_point = self.swh.get_pin_point(end_name)
        end_pin_distance = int(end_insert_point[0])
        return beg_pin_distance, end_pin_distance, end_name

    def get_ww_pin_to_edge(self, pin_name, edge):
        beg_insert_point = self.swh.get_pin_point(pin_name)
        beg_pin_distance = int(beg_insert_point[0])
        end_name = pin_name.replace("beg", "end").replace("BEG", "END")
        end_insert_point = self.swh.get_pin_point(end_name)
        end_pin_distance = int(edge - end_insert_point[0])
        return beg_pin_distance, end_pin_distance, end_name

    def get_nn_pin_to_edge(self, pin_name, edge):
        beg_insert_point = self.swh.get_pin_point(pin_name)
        beg_pin_distance = int(edge - beg_insert_point[1])
        end_name = pin_name.replace("beg", "end").replace("BEG", "END")
        end_insert_point = self.swh.get_pin_point(end_name)
        end_pin_distance = int(end_insert_point[1])
        return beg_pin_distance, end_pin_distance, end_name

    def get_ss_pin_to_edge(self, pin_name, edge):
        beg_insert_point = self.swh.get_pin_point(pin_name)
        beg_pin_distance = int(beg_insert_point[1])
        end_name = pin_name.replace("beg", "end").replace("BEG", "END")
        end_insert_point = self.swh.get_pin_point(end_name)
        end_pin_distance = int(edge - end_insert_point[1])
        return beg_pin_distance, end_pin_distance, end_name

    def create_line(self):

        units, grid = calculate_line.process_units()
        row_distances, col_distances = calculate_line.calculate_distances(grid)

        unique_row_logical_distances = calculate_line.unique_distances(row_distances)
        unique_col_logical_distances = calculate_line.unique_distances(col_distances)

        self.create_line_points(unique_row_logical_distances)
        # self.create_line_points("SWHR")
        self.create_ns_line(unique_col_logical_distances)

    # Line in config must from small to large
    def create_line_points(self, logical_distances):
        for section in self.config.down_layout:
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
                width = self.config.get_width()

                for index, combination in enumerate(length_combinations):
                    chip_view_graphic.normalLine_e_map[combination] = []
                    single_line_start_y = line_group_start_y
                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [(0, 0)]

                        x = 0
                        y = single_line_start_y
                        beg_to_edge, edge_to_end, end_name = self.get_ee_pin_to_edge(pin_name, width)

                        for i in range(stair_num):
                            count = count + 1
                            x = x
                            y = single_line_start_y - drop_height * i
                            point_list.append((x, y))

                            count = count + 1
                            if count == point_num - 1:
                                x = beg_to_edge + (sum(combination) - 1) * (width + self.space) \
                                    + self.space + edge_to_end
                            else:
                                x = beg_to_edge + (sum(combination[:i+1]) - 1) * (width + self.space) + self.space\
                                    + width / 2 - self.multi * line_group_num * i - self.multi * pin_index

                            y = y
                            point_list.append((x, y))
                        block_name = pin_name + "-" + end_name + "-" + str(index)
                        self.line_r_list.append(block_name)

                        point_list.append((x, 0))
                        single_line_start_y = single_line_start_y - self.gap
                        self.min_y = y
                        normal_line_block = self.dwg.blocks.new(name=block_name)
                        normal_line_block.add_lwpolyline(point_list)
                        chip_view_graphic.normalLine_e_map[combination].append(block_name)

        for section in self.config.up_layout:
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
                width = self.config.get_width()

                for index, combination in enumerate(length_combinations):
                    chip_view_graphic.normalLine_w_map[combination] = []
                    single_line_start_y = line_group_start_y
                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [(0, 0)]

                        x = 0
                        y = single_line_start_y
                        beg_to_edge, edge_to_end, end_name = self.get_ww_pin_to_edge(pin_name, width)

                        for i in range(stair_num):
                            count = count + 1
                            x = x
                            y = single_line_start_y + rise_height * i
                            point_list.append((x, y))

                            count = count + 1
                            if count == point_num - 1:
                                x = 0 - (beg_to_edge + (sum(combination) - 1) * (width + self.space)
                                         + self.space + edge_to_end)
                            else:
                                x = 0 - (beg_to_edge + (sum(combination[:i + 1]) - 1) * (width + self.space) + self.space
                                         + width / 2 - self.multi * line_group_num * i - self.multi * pin_index)

                            y = y
                            point_list.append((x, y))
                        block_name = pin_name + "-" + end_name + "-" + str(index)
                        self.line_r_list.append(block_name)

                        point_list.append((x, 0))
                        single_line_start_y = single_line_start_y + self.gap
                        self.max_y = y
                        normal_line_block = self.dwg.blocks.new(name=block_name)
                        normal_line_block.add_lwpolyline(point_list)
                        chip_view_graphic.normalLine_w_map[combination].append(block_name)

    def create_ns_line(self, logic_distances):
        for section in self.config.left_layout:
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
                height = self.config.get_height()

                for index, combination in enumerate(length_combinations):
                    chip_view_graphic.normalLine_n_map[combination] = []
                    single_line_start_x = line_group_start_x
                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [(0, 0)]

                        x = single_line_start_x
                        y = 0
                        beg_to_edge, edge_to_end, end_name = self.get_nn_pin_to_edge(pin_name, height)

                        for i in range(stair_num):
                            count = count + 1
                            x = single_line_start_x - ext_width * i
                            y = y
                            point_list.append((x, y))

                            count = count + 1
                            if count == point_num - 1:
                                y = beg_to_edge + (sum(combination) - 1) * (height + self.space) \
                                    + self.space + edge_to_end
                            else:
                                y = beg_to_edge + (sum(combination[:i+1]) - 1) * (height + self.space) + self.space \
                                    + height / 2 - self.multi * line_group_num * i - self.multi * pin_index

                            x = x
                            point_list.append((x, y))
                        block_name = pin_name + "-" + end_name + "-" + str(index)
                        self.line_r_list.append(block_name)

                        point_list.append((0, y))
                        single_line_start_x = single_line_start_x - self.gap
                        self.min_x = x
                        normal_line_block = self.dwg.blocks.new(name=block_name)
                        normal_line_block.add_lwpolyline(point_list)
                        chip_view_graphic.normalLine_n_map[combination].append(block_name)

        for section in self.config.right_layout:
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
                height = self.config.get_height()

                for index, combination in enumerate(length_combinations):
                    chip_view_graphic.normalLine_s_map[combination] = []
                    single_line_start_x = line_group_start_x
                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [(0, 0)]

                        x = single_line_start_x
                        y = 0
                        beg_to_edge, edge_to_end, end_name = self.get_ss_pin_to_edge(pin_name, height)

                        for i in range(ext_num + 1):
                            count = count + 1
                            x = single_line_start_x + ext_width * i
                            y = y
                            point_list.append((x, y))

                            count = count + 1
                            if count == point_num - 1:
                                y = 0 - (beg_to_edge + (sum(combination) - 1) * (height + self.space)
                                         + self.space + edge_to_end)
                            else:
                                y = 0 - (beg_to_edge + (sum(combination[:i+1]) - 1) * (height + self.space) + self.space
                                         + height / 2 - self.multi * line_group_num * i - self.multi * pin_index)

                            x = x
                            point_list.append((x, y))
                        block_name = pin_name + "-" + end_name + "-" + str(index)
                        self.line_r_list.append(block_name)

                        point_list.append((0, y))
                        single_line_start_x = single_line_start_x + self.gap
                        self.max_x = x
                        normal_line_block = self.dwg.blocks.new(name=block_name)
                        normal_line_block.add_lwpolyline(point_list)
                        chip_view_graphic.normalLine_s_map[combination].append(block_name)
