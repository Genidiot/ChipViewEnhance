import ezdxf
from src.Parser import ParserSWH
from src.Parser.ParserSWH import Layout
from typing import cast


class SwhCreate:
    def __init__(self, config: ParserSWH.SwhConfig, dwg):
        self.dwg = dwg
        ezdxf.setup_linetypes(self.dwg)
        self.msp = self.dwg.modelspace()
        self.config = config

        self.create_rect()

    def create_rect(self):
        tile_name = self.config.tile_type
        width = self.config.width
        height = self.config.height
        swh_block = self.dwg.blocks.new(name=tile_name)
        swh_block.add_line((0, 0), (width, 0))
        swh_block.add_line((width, 0), (width, height))
        swh_block.add_line((width, height), (0, height))
        swh_block.add_line((0, height), (0, 0))

        self.create_pins(swh_block)

    def create_pins(self, swh_block):
        mux_width = self.config.mux_width
        edge_space = self.config.edge_space
        part_length = self.config.width / self.config.part_num

        for section in self.config.down_layout:
            index = section.part_index
            group_space = section.group_space
            direction = section.direction

            if index == 0:
                left = index * part_length + edge_space - 2
                location = left
            elif index == 9:
                right = (index + 1) * part_length - edge_space + 2
                location = right
            else:
                left = index * part_length + 2
                location = left

            for Mux in section.mux_group_list:
                location = location + direction * group_space
                for name in Mux.mux_name:
                    pin = self.dwg.blocks.new(name)
                    pin.add_circle((0, 0), mux_width / 2)
                    swh_block.add_blockref(name, (location, 0))
                    location = location + direction * mux_width

        for section in self.config.up_layout:
            index = section.part_index
            group_space = section.group_space
            direction = section.direction

            if index == 0:
                left = index * part_length + edge_space - 2
                location = left
            elif index == 9:
                right = (index + 1) * part_length - edge_space + 2
                location = right
            else:
                left = index * part_length + 2
                location = left

            for Mux in section.mux_group_list:
                location = location + direction * group_space
                for name in Mux.mux_name:
                    pin = self.dwg.blocks.new(name)
                    pin.add_circle((0, 0), mux_width / 2)
                    swh_block.add_blockref(name, (location, self.config.height))
                    location = location + direction * mux_width

        for section in self.config.left_layout:
            index = section.part_index
            group_space = section.group_space
            direction = section.direction

            if index == 0:
                low = index * part_length + edge_space - 2
                location = low
            elif index == 9:
                high = (index + 1) * part_length - edge_space + 2
                location = high
            else:
                low = index * part_length + 2
                location = low

            for Mux in section.mux_group_list:
                location = location + direction * group_space
                for name in Mux.mux_name:
                    pin = self.dwg.blocks.new(name)
                    pin.add_circle((0, 0), mux_width / 2)
                    swh_block.add_blockref(name, (0, location))
                    location = location + direction * mux_width

        for section in self.config.right_layout:
            index = section.part_index
            group_space = section.group_space
            direction = section.direction

            if index == 0:
                low = index * part_length + edge_space - 2
                location = low
            elif index == 9:
                high = (index + 1) * part_length - edge_space + 2
                location = high
            else:
                low = index * part_length + 2
                location = low

            for Mux in section.mux_group_list:
                location = location + direction * group_space
                for name in Mux.mux_name:
                    pin = self.dwg.blocks.new(name)
                    pin.add_circle((0, 0), mux_width / 2)
                    swh_block.add_blockref(name, (self.config.width, location))
                    location = location + direction * mux_width

    def get_sub_block_insert(self, pinname):
        for e in self.dwg.blocks:
            for entity in e:
                if entity.dxftype() == "INSERT":
                    blockref = cast("Insert", entity)
                    if blockref.dxf.name == pinname:
                        return blockref.dxf.insert

    def save_as(self, filename: str):
        self.dwg.saveas(filename=filename)
