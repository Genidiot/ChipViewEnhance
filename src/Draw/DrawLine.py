import ezdxf
from src.ParserJson import ParserSWH
from src.ParserJson.ParserSWH import Layout
from src.ParserJson.ParserSWH import MuxNames
from src.Draw import DrawSWH
from typing import cast
import re


def get_group(group_name: str):
    if group_name.find("L1Beg") != -1:
        return 1
    elif group_name.find("L2Beg") != -1:
        return 2
    elif group_name.find("L4Beg") != -1:
        return 4
    elif group_name.find("L6Beg") != -1:
        return 6
    elif group_name.find("L12Beg") != -1:
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
        end_name = pin_name.replace("beg", "end")
        end_insert_point = self.swh.get_pin_point(end_name)
        end_pin_distance = int(end_insert_point[0])
        return beg_pin_distance, end_pin_distance, end_name

    def get_ww_pin_to_edge(self, pin_name, edge):
        beg_insert_point = self.swh.get_pin_point(pin_name)
        beg_pin_distance = int(beg_insert_point[0])
        end_name = pin_name.replace("beg", "end")
        end_insert_point = self.swh.get_pin_point(end_name)
        end_pin_distance = int(edge - end_insert_point[0])
        return beg_pin_distance, end_pin_distance, end_name

    def get_nn_pin_to_edge(self, pin_name, edge):
        beg_insert_point = self.swh.get_pin_point(pin_name)
        beg_pin_distance = int(edge - beg_insert_point[1])
        end_name = pin_name.replace("beg", "end")
        end_insert_point = self.swh.get_pin_point(end_name)
        end_pin_distance = int(end_insert_point[1])
        return beg_pin_distance, end_pin_distance, end_name

    def get_ss_pin_to_edge(self, pin_name, edge):
        beg_insert_point = self.swh.get_pin_point(pin_name)
        beg_pin_distance = int(beg_insert_point[1])
        end_name = pin_name.replace("beg", "end")
        end_insert_point = self.swh.get_pin_point(end_name)
        end_pin_distance = int(edge - end_insert_point[1])
        return beg_pin_distance, end_pin_distance, end_name

    def create_line(self):
        self.create_line_points("SWHL")
        self.create_line_points("SWHR")
        self.create_ns_line()

    # Line in config must from small to large
    def create_line_points(self, tile_type):
        self.min_y = -99
        self.max_y = 99
        for section in self.config.down_layout:
            section: Layout
            if section.get_index() != 9:
                continue
            for Mux in section.mux_group_list:
                Mux: MuxNames
                line_length = get_group(Mux.group_name)
                if line_length != -1:
                    line_num = len(Mux.mux_name)
                    drop_height = line_num
                    drop_num = line_length - 1
                    point_num = line_length * 2 + 2
                    start_y = self.min_y - self.gap
                    width = self.config.get_width()

                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [(0, 0)]
                        x = 0
                        y = start_y

                        beg_to_edge, edge_to_end, end_name = self.get_ee_pin_to_edge(pin_name, width)

                        if tile_type[3] == "R":
                            for i in range(drop_num + 1):
                                count = count + 1
                                x = x
                                y = start_y - drop_height * i
                                point_list.append((x, y))

                                count = count + 1
                                if count == point_num - 1:
                                    if line_length % 2 == 0:
                                        x = beg_to_edge + (line_length * 2 - 1) * (width + self.space) \
                                            + self.space + edge_to_end
                                    else:
                                        x = beg_to_edge + line_length * 2 * (width + self.space) \
                                            + self.space + edge_to_end
                                else:
                                    if i % 2 == 0:
                                        x = int(beg_to_edge + (2 * i + 2) * (width + self.space) + self.space
                                                + width / 2 - self.multi * line_num * i - self.multi * pin_index)
                                    else:
                                        x = int(beg_to_edge + (2 * i + 1) * (width + self.space) + self.space
                                                + width / 2 - self.multi * line_num * i - self.multi * pin_index)
                                y = y
                                point_list.append((x, y))
                            block_name = pin_name + "-" + end_name + "-" + tile_type[3]
                            self.line_r_list.append(block_name)

                        elif tile_type[3] == "L":
                            for i in range(drop_num + 1):
                                count = count + 1
                                x = x
                                y = start_y - drop_height * i
                                point_list.append((x, y))

                                count = count + 1
                                if count == point_num - 1:
                                    if line_length % 2 == 0:
                                        x = beg_to_edge + (line_length * 2 - 1) * (width + self.space) \
                                            + self.space + edge_to_end
                                    else:
                                        x = beg_to_edge + (line_length * 2 - 2) * (width + self.space) \
                                            + self.space + edge_to_end
                                else:
                                    if i % 2 == 0:
                                        x = int(beg_to_edge + (2 * i) * (width + self.space) + self.space
                                                + width / 2 - self.multi * line_num * i - self.multi * pin_index)
                                    else:
                                        x = int(beg_to_edge + (2 * i + 1) * (width + self.space) + self.space
                                                + width / 2 - self.multi * line_num * i - self.multi * pin_index)
                                y = y
                                point_list.append((x, y))
                            block_name = pin_name + "-" + end_name + "-" + tile_type[3]
                            self.line_l_list.append(block_name)

                        point_list.append((x, 0))
                        start_y = start_y - self.gap
                        self.min_y = y
                        normal_line_block = self.dwg.blocks.new(name=block_name)
                        normal_line_block.add_lwpolyline(point_list)

        for section in self.config.up_layout:
            if section.get_index() != 0:
                continue
            for Mux in section.mux_group_list:
                line_length = get_group(Mux.group_name)
                if line_length != -1:
                    line_num = len(Mux.mux_name)
                    rise_height = line_num
                    rise_num = line_length - 1
                    point_num = line_length * 2 + 2
                    start_y = self.max_y + self.gap
                    width = self.config.get_width()

                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [(0, 0)]
                        x = 0
                        y = start_y

                        beg_to_edge, edge_to_end, end_name = self.get_ww_pin_to_edge(pin_name, width)

                        if tile_type[3] == "R":
                            for i in range(rise_num + 1):
                                count = count + 1
                                x = x
                                y = start_y + rise_height * i
                                point_list.append((x, y))

                                count = count + 1
                                if count == point_num - 1:
                                    if line_length % 2 == 0:
                                        x = 0 - (beg_to_edge + (line_length * 2 - 1) * (width + self.space)
                                                 + self.space + edge_to_end)
                                    else:
                                        x = 0 - (beg_to_edge + (line_length * 2 - 2) * (width + self.space)
                                                 + self.space + edge_to_end)
                                else:
                                    if i % 2 == 0:
                                        x = 0 - int(beg_to_edge + (2 * i) * (width + self.space) + self.space
                                                    + width / 2 - self.multi * line_num * i - self.multi * pin_index)
                                    else:
                                        x = 0 - int(beg_to_edge + (2 * i + 1) * (width + self.space) + self.space
                                                    + width / 2 - self.multi * line_num * i - self.multi * pin_index)
                                y = y
                                point_list.append((x, y))
                            block_name = pin_name + "-" + end_name + "-" + tile_type[3]
                            self.line_r_list.append(block_name)

                        elif tile_type[3] == "L":
                            for i in range(rise_num + 1):
                                count = count + 1
                                x = x
                                y = start_y + rise_height * i
                                point_list.append((x, y))

                                count = count + 1
                                if count == point_num - 1:
                                    if line_length % 2 == 0:
                                        x = 0 - (beg_to_edge + (line_length * 2 - 1) * (width + self.space)
                                                 + self.space + edge_to_end)
                                    else:
                                        x = 0 - (beg_to_edge + (line_length * 2) * (width + self.space)
                                                 + self.space + edge_to_end)
                                else:
                                    if i % 2 == 0:
                                        x = 0 - int(beg_to_edge + (2 * i + 2) * (width + self.space) + self.space
                                                    + width / 2 - self.multi * line_num * i - self.multi * pin_index)
                                    else:
                                        x = 0 - int(beg_to_edge + (2 * i + 1) * (width + self.space) + self.space
                                                    + width / 2 - self.multi * line_num * i - self.multi * pin_index)
                                y = y
                                point_list.append((x, y))
                            block_name = pin_name + "-" + end_name + "-" + tile_type[3]
                            self.line_l_list.append(block_name)

                        point_list.append((x, 0))
                        start_y = start_y + self.gap
                        self.max_y = y
                        normal_line_block = self.dwg.blocks.new(name=block_name)
                        normal_line_block.add_lwpolyline(point_list)

    def create_ns_line(self):
        for section in self.config.left_layout:
            section: Layout
            if section.get_index() != 9:
                continue
            for Mux in section.mux_group_list:
                Mux: MuxNames
                line_length = get_group(Mux.group_name)
                if line_length != -1:
                    line_num = len(Mux.mux_name)
                    ext_width = line_num
                    ext_num = line_length - 1
                    point_num = line_length * 2 + 2
                    start_x = self.min_x - self.gap
                    height = self.config.get_height()

                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [(0, 0)]
                        x = start_x
                        y = 0

                        beg_to_edge, edge_to_end, end_name = self.get_nn_pin_to_edge(pin_name, height)
                        block_name = ""
                        for i in range(ext_num + 1):
                            count = count + 1
                            x = start_x - ext_width * i
                            y = y
                            point_list.append((x, y))

                            count = count + 1
                            x = x
                            if count == point_num - 1:
                                y = beg_to_edge + (line_length - 1) * (height + self.space) \
                                    + self.space + edge_to_end
                            else:
                                y = int(beg_to_edge + i * (height + self.space) + self.space
                                        + height / 2 - self.multi * line_num * i - self.multi * pin_index)
                            point_list.append((x, y))
                        block_name = pin_name + "-" + end_name
                        self.line_r_list.append(block_name)
                        self.line_l_list.append(block_name)

                        point_list.append((0, y))
                        start_x = start_x - self.gap
                        self.min_x = x
                        normal_line_block = self.dwg.blocks.new(name=block_name)
                        normal_line_block.add_lwpolyline(point_list)

        for section in self.config.right_layout:
            section: Layout
            if section.get_index() != 0:
                continue
            for Mux in section.mux_group_list:
                Mux: MuxNames
                line_length = get_group(Mux.group_name)
                if line_length != -1:
                    line_num = len(Mux.mux_name)
                    ext_width = line_num
                    ext_num = line_length - 1
                    point_num = line_length * 2 + 2
                    start_x = self.max_x + self.gap
                    height = self.config.get_height()

                    for pin_name in Mux.mux_name:
                        pin_index = extract_number(pin_name)
                        count = 1
                        point_list = [(0, 0)]
                        x = start_x
                        y = 0

                        beg_to_edge, edge_to_end, end_name = self.get_ss_pin_to_edge(pin_name, height)
                        block_name = ""
                        for i in range(ext_num + 1):
                            count = count + 1
                            x = start_x + ext_width * i
                            y = y
                            point_list.append((x, y))

                            count = count + 1
                            x = x
                            if count == point_num - 1:
                                y = 0 - (beg_to_edge + (line_length - 1) * (height + self.space)
                                         + self.space + edge_to_end)
                            else:
                                y = 0 - int(beg_to_edge + i * (height + self.space) + self.space
                                            + height / 2 - self.multi * line_num * i - self.multi * pin_index)
                            point_list.append((x, y))
                            block_name = pin_name + "-" + end_name
                            self.line_r_list.append(block_name)
                            self.line_l_list.append(block_name)

                        point_list.append((0, y))
                        start_x = start_x + self.gap
                        self.max_x = x
                        normal_line_block = self.dwg.blocks.new(name=block_name)
                        normal_line_block.add_lwpolyline(point_list)
