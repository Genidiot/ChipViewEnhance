from src.DataBase.graphic import chip_view_graphic
import numpy as np


def process_units():
    units = chip_view_graphic.swh_point_map
    grid = initialize_grid(units)
    grid = fill_grid(grid, units)
    return units, grid


def initialize_grid(units):
    # 找到网格的最大尺寸
    max_x = max(unit[0] for unit in units) + 1
    max_y = max(unit[1] for unit in units) + 1
    grid = np.empty((max_y, max_x), dtype=object)
    grid.fill(None)
    return grid


def fill_grid(grid, units):
    for x, y in units:
        grid[y][x] = (x, y)
    return grid


def calculate_distances(grid):
    row_distances = {}
    col_distances = {}

    for y in range(grid.shape[0]):
        row_units = [grid[y][x] for x in range(grid.shape[1]) if grid[y][x] is not None]
        if row_units:
            physical_distances = calculate_physical_distances(row_units, 'x')
            logical_distances = calculate_all_logical_distances(row_units, 'x')
            row_distances[y] = {
                "physical_distances": physical_distances,
                "logical_distances": logical_distances
            }

    for x in range(grid.shape[1]):
        col_units = [grid[y][x] for y in range(grid.shape[0]) if grid[y][x] is not None]
        if col_units:
            physical_distances = calculate_physical_distances(col_units, 'y')
            logical_distances = calculate_all_logical_distances(col_units, 'y')
            col_distances[x] = {
                "physical_distances": physical_distances,
                "logical_distances": logical_distances
            }

    return row_distances, col_distances


def calculate_physical_distances(units, direction='x'):
    distances = []
    for i in range(len(units) - 1):
        if direction == 'x':
            distances.append(units[i+1][0] - units[i][0])
        elif direction == 'y':
            distances.append(units[i+1][1] - units[i][1])
    return distances


def calculate_all_logical_distances(units, direction='x'):
    max_logical_distance = min(len(units)-1, 15)
    dict_distance = {}
    for logical_distance in range(1, max_logical_distance + 1):
        dict_distance[logical_distance] = []
        distance_combinations = set()
        for i in range(len(units) - logical_distance):
            combination = []
            for j in range(logical_distance):
                if direction == 'x':
                    combination.append(units[i+j+1][0] - units[i+j][0])
                elif direction == 'y':
                    combination.append(units[i+j+1][1] - units[i+j][1])
            distance_combinations.add(tuple(combination))
        dict_distance[logical_distance] = list(distance_combinations)
    return dict_distance


def unique_distances(distances):
    unique_logical_distances = {}
    for dist in distances.values():
        for logical_distance, combinations in dist['logical_distances'].items():
            if logical_distance not in unique_logical_distances:
                unique_logical_distances[logical_distance] = set()
            unique_logical_distances[logical_distance].update(combinations)
    return {k: list(v) for k, v in unique_logical_distances.items()}


def calculate_logical_distances_from_unit(grid, start_unit, direction='x'):
    if direction == 'x':
        y = start_unit[1]
        row_units = [grid[y][x] for x in range(grid.shape[1]) if grid[y][x] is not None]
        row_units.sort()
        start_index = row_units.index(start_unit)
        subsequent_units = row_units[start_index:]
    else:
        x = start_unit[0]
        col_units = [grid[y][x] for y in range(grid.shape[0]) if grid[y][x] is not None]
        col_units.sort(key=lambda pos: pos[1])
        start_index = col_units.index(start_unit)
        subsequent_units = col_units[start_index:]

    return calculate_certain_logical_distances(subsequent_units, direction)


def calculate_certain_logical_distances(units, direction='x'):
    max_logical_distance = min(len(units)-1, 15)
    dict_distance = {}
    for logical_distance in range(1, max_logical_distance + 1):
        dict_distance[logical_distance] = []
        combination = []
        for i in range(logical_distance):
            if direction == 'x':
                combination.append(units[i+1][0] - units[i][0])
            elif direction == 'y':
                combination.append(units[i+1][1] - units[i][1])
        dict_distance[logical_distance].append(tuple(combination))
    return dict_distance
