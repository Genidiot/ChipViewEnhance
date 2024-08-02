import json


class MuxNames:
    def __init__(self, group_name: str, mux_name: list):
        self.group_name = group_name
        self.mux_name = mux_name

    def get_mux_name_list(self):
        return self.mux_name


class Layout:
    def __init__(self, part_index=0, group_space=0, direction=0):
        self.part_index = part_index
        self.group_space = group_space
        self.direction = direction
        self.mux_group_list = []

    def add_group(self, names: MuxNames):
        self.mux_group_list.append(names)

    def get_index(self):
        return self.part_index


class SwhConfig:
    def __init__(self, filename):
        self.filename = filename
        self.tile_type = ""
        self.width = 0
        self.height = 0
        self.part_num = 0
        self.mux_width = 0
        self.edge_space = 0
        self.down_layout = list()
        self.up_layout = list()
        self.left_layout = list()
        self.right_layout = list()

        self.__read_config()

    def __read_config(self):
        with open(self.filename, 'r') as configfile:
            configuration = json.load(configfile)
        self.__parser_config(configuration)

    def __parser_config(self, configuration: dict):
        self.tile_type = configuration["tileType"]
        self.width = configuration["width"]
        self.height = configuration["height"]
        self.part_num = configuration["partNum"]
        self.mux_width = configuration["muxWidth"]
        self.edge_space = configuration["edgeSpace"]

        for section in configuration["downLayout"]:
            temp_mux_groups = Layout(section["partIndex"], section["groupSpace"], section["direction"])
            for nameList in section["muxGroupList"]:
                group_names = MuxNames(nameList["muxGroupName"], nameList["muxName"])
                temp_mux_groups.add_group(group_names)
            self.down_layout.append(temp_mux_groups)

        for section in configuration["upLayout"]:
            temp_mux_groups = Layout(section["partIndex"], section["groupSpace"], section["direction"])
            for nameList in section["muxGroupList"]:
                group_names = MuxNames(nameList["muxGroupName"], nameList["muxName"])
                temp_mux_groups.add_group(group_names)
            self.up_layout.append(temp_mux_groups)

        for section in configuration["leftLayout"]:
            temp_mux_groups = Layout(section["partIndex"], section["groupSpace"], section["direction"])
            for nameList in section["muxGroupList"]:
                group_names = MuxNames(nameList["muxGroupName"], nameList["muxName"])
                temp_mux_groups.add_group(group_names)
            self.left_layout.append(temp_mux_groups)

        for section in configuration["rightLayout"]:
            temp_mux_groups = Layout(section["partIndex"], section["groupSpace"], section["direction"])
            for nameList in section["muxGroupList"]:
                group_names = MuxNames(nameList["muxGroupName"], nameList["muxName"])
                temp_mux_groups.add_group(group_names)
            self.right_layout.append(temp_mux_groups)

    def get_type(self):
        return self.tile_type

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_mux_width(self):
        return self.mux_width

    def get_down_layout(self):
        return self.down_layout
