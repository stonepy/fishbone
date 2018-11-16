import time

import random



class environment:
    """ Define Environment Attributes """

    def __init__(self):
        self.temperature = 30  # Degree


class cell_type_0:
    """ Define Cell Type 1 Attributes """

    def __init__(self):
        self.symbol = "*"
        self.divide_rate = 1  # Max is 1, Min is 0. RATE = Divide Once / Refresh Times
        self.priority = 1  # Max is 10, Min is 0.
        self.invasive = 0  # Max is 10, Min is 0.

        self.divide_direction = {

            "left_1": [0.0000, 0.0625],
            "top-left": [0.0625, 0.1875],
            "top": [0.1875, 0.3125],
            "top-right": [0.3125, 0.4375],
            "right": [0.4375, 0.5625],
            "bottom-right": [0.5625, 0.6875],
            "bottom": [0.6875, 0.8125],
            "bottom-left": [0.8125, 0.9375],
            "left_2": [0.9375, 1.0000],

        }

        self.tranform = [
            "type_1",
            "type_2",
            "type_3",
            "type_4",
            "type_5",
            "type_6",
            "type_7",
            "type_8",
        ]



# Produce Blank Plate For Cells To Grow
def plate_producer(width, height):

    white_plate = []
    for row in range(height):
        white_plate.append(["."] * width)

    return white_plate


# Plant Cells On White Plate
def cell_planter(cells_on_plate, plate):

    width  = len(plate[0])
    height = len(plate)

    for cell in cells_on_plate:
        for pos in cells_on_plate[cell]:
            if len(pos) == 0:
                continue
            else:
                if 0 <= pos[0] & pos[0] <= width - 1 and 0 <= pos[1] & pos[1] <= height - 1:
                    plate[pos[1]][pos[0]] = cell

    return plate


# Decide Which Direction To Divide
def divide_direction_decide(divide_direction):

    rand_num = random.random()

    for direct in divide_direction:
        direct_range = divide_direction[direct]
        if rand_num > direct_range[0] and rand_num < direct_range[1]:
            direction = direct.split("_")[0]

    return direction


# Divide Cell
def divide(current_position, direction):

    curr_pos = current_position

    direct_pos_table = {

        "left": [curr_pos[1] + 0, curr_pos[0] - 1],
        "top-left": [curr_pos[1] - 1, curr_pos[0] - 1],
        "top": [curr_pos[1] - 1, curr_pos[0] + 0],
        "top-right": [curr_pos[1] - 1, curr_pos[0] + 1],
        "right": [curr_pos[1] + 0, curr_pos[0] + 1],
        "bottom-right": [curr_pos[1] + 1, curr_pos[0] + 1],
        "bottom": [curr_pos[1] + 1, curr_pos[0] + 0],
        "bottom-left": [curr_pos[1] + 1, curr_pos[0] - 1],

    }

    divide_position = direct_pos_table[direction]

    return divide_position


# Update Status Of Cells Growing On The Plate
def update(plate, cell_all, cell_set):

    plate_cell_pos = cell_all.values()
    width  = len(plate[0])
    height = len(plate)

    for h in range(height):
        for w in range(width):
            symbol = plate[h][w]
            if symbol not in cell_set:
                continue

            cell = cell_set[symbol]

            direction  = divide_direction_decide(cell.divide_direction)
            divide_pos = divide([h, w], direction)

            if divide_pos not in plate_cell_pos:
                cell_all[symbol].append(divide_pos)

    return cell_all



""" Game Start Here """
def main():

    refresh_interval = 1  # Second
    width, height = 50, 30  # Point
    start_cells = {

        "*": [[24, 7]],
        "#": [],
        "%": [],
        "&": [],
        "@": [],
        "%": [],

    }

    cell_set = {

        "*": cell_type_0(),
        "#": None,
        "%": None,
        "&": None,
        "@": None,
        "%": None,

    }

    cell_all = start_cells
    white_plate = plate_producer(width, height)
    plate = cell_planter(start_cells, white_plate)

    for row in plate:
        print(" ".join(row))
    print("\n")

    # Growth Start
    while True:
        for symbol in cell_set:

            if cell_set[symbol] != None:

                cell_all = update(plate, cell_all, cell_set)
                plate = cell_planter(cell_all, plate)

        for row in plate:
            print(" ".join(row))
        print("\n")

        time.sleep(refresh_interval)


main()
