import ezdxf
from src.Parser import ParserSWH
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
    def __init__(self, config: ParserSWH.SwhConfig, swh: DrawSWH.SwhCreate, dwg):
        self.dwg = dwg
        self.msp = self.dwg.modelspace()
        self.config = config
        self.swh = swh

        self.drop_height = 0
        self.drop_num = 0
        self.gap = 1
        self.min_y = -99

        self.create_line_points()

    # Line in config must from small to large
    def create_line_points(self):
        mix_y = -99
        max_y = 99
        for section in self.config.down_layout:
            for Mux in section.mux_group_list:
                line_length = get_group(Mux.group_name)
                if line_length != -1:
                    line_num = len(Mux.mux_name)
                    self.drop_height = line_num
                    self.drop_num = line_length - 1
                    point_num = line_length * 2 + 2
                    start_y = self.min_y - self.gap
                    for name in Mux.mux_name:
                        index = extract_number(name)
                        count = 1
                        point_list = [(0, 0)]
                        x = 0
                        y = start_y

                        for i in range(self.drop_num + 1):
                            count = count + 1
                            x = x
                            y = start_y - self.drop_height * i
                            point_list.append((x, y))
                            count = count + 1
                            # print(count)

                            point = self.swh.get_sub_block_insert(name)
                            juli = int((2000 - point[0]))

                            if count == point_num - 1:
                                if line_length % 2 == 0:
                                    x = (line_length * 2 - 1) * 3000 + 1000 + juli * 2
                                else:
                                    x = line_length * 2 * 3000 + 1000 + juli * 2
                            else:
                                if i % 2 == 0:
                                    x = (2 * i + 2) * 3000 + 1000 + 1000 - 4 * line_num * i - 4 * index + juli
                                else:
                                    x = (2 * i + 1) * 3000 + 1000 + 1000 - 4 * line_num * i - 4 * index + juli
                            y = y
                            point_list.append((x, y))

                        point_list.append((x, 0))
                        start_y = start_y - self.gap
                        self.min_y = y
                        print(Mux.group_name, name, point_list)
