# Code written by Alexander Holmstock

import numpy as np
from PIL import Image
import random


class Map(object):
    def __init__(self, size):
        self.map_list = []
        self.size = size
        # self.map_list = np.zeros((size, size))
        self.size = size
        for _ in range(0, size):
            temp = []
            for _ in range(0, size):
                temp.append(0)
            self.map_list.append(temp)
        self.terraform()
        self.generate_map_image("gamemap.png")

    def print_map(self):
        for x in self.map_list:
            line = ""
            for y in x:
                line += str(y) + " "
            print(line)

    def return_map(self):
        map_string = ""
        for x in self.map_list:
            line = ""
            for y in x:
                line += str(y) + " "
            map_string += line + "\n"
        return map_string

    # on our maps, 0 will represent forest, 1 will represent a clear plane, 2 will represent a lake, 3 will represent
    # a mountain, and 4 will represent a river
    def terraform(self):
        # if the map is 10x10 or larger we can have a river
        if self.size >= 10:
            north_or_west_origin = random.randint(0, 1)  # randomly decide which direction the river will flow from
            river_width = self.size // 10
            if north_or_west_origin == 0:  # 0 means north, 1 means west
                river_location = random.randint(0, self.size - 1)
                for x in range(self.size):
                    # 25 percent change to initiate RIVER DRIFT(this is just the river wiggling so it looks natural)
                    river_drift = random.randint(0, 3)
                    # when it drifts, it always tends toward the center to give the river a natural curve
                    if river_drift == 0:
                        if river_location > self.size / 2:
                            river_location -= 1
                        else:
                            river_location += 1
                    for y in range(river_width):
                        if river_location + y <= self.size - 1:
                            self.map_list[x][river_location + y] = 4
            else:
                river_location = random.randint(0, self.size - 1)
                for x in range(self.size):
                    river_drift = random.randint(0, 3)
                    if river_drift == 1:
                        if river_location > self.size / 2:
                            river_location -= 1
                        else:
                            river_location += 1
                    for y in range(river_width):
                        if river_location + y <= self.size - 1:
                            self.map_list[river_location + y][x] = 4

    # to generate the map we're gonna make a numpy array where each coordinate on the map is a 5x5 part of the array
    # the coordinates will have the rgb values in an array
    # 0 = forest = 27,122,49
    # 1 = plane = 45,220,86
    # 2 = lake = 45,180,220
    # 3 = mountain = 176,176,176
    # 4 = river = 44,115,220
    def generate_map_image(self, filename):
        image_array = np.zeros((self.size * 5, self.size * 5, 3), dtype=np.uint8)
        for x in range(self.size):
            for y in range(self.size):
                if self.map_list[x][y] == 0:
                    color = [27, 122, 49]
                elif self.map_list[x][y] == 1:
                    color = [45, 220, 86]
                elif self.map_list[x][y] == 2:
                    color = [45, 180, 220]
                elif self.map_list[x][y] == 3:
                    color = [176, 176, 176]
                elif self.map_list[x][y] == 4:
                    color = [44, 115, 220]
                else:
                    color = [255, 0, 0]
                image_array[5 * x][5 * y] = image_array[5 * x + 1][5 * y] = image_array[5 * x + 2][5 * y] = \
                    image_array[5 * x + 3][5 * y] = image_array[5 * x + 4][5 * y] = image_array[5 * x][5 * y + 1] \
                    = image_array[5 * x + 1][5 * y + 1] = image_array[5 * x + 2][5 * y + 1] = \
                    image_array[5 * x + 3][5 * y + 1] = image_array[5 * x + 4][5 * y + 1] = image_array[5 * x][
                    5 * y + 2] \
                    = image_array[5 * x + 1][5 * y + 2] = image_array[5 * x + 2][5 * y + 2] = \
                    image_array[5 * x + 3][5 * y + 2] = image_array[5 * x + 4][5 * y + 2] = image_array[5 * x][
                    5 * y + 3] \
                    = image_array[5 * x + 1][5 * y + 3] = image_array[5 * x + 2][5 * y + 3] = \
                    image_array[5 * x + 3][5 * y + 3] = image_array[5 * x + 4][5 * y + 3] = image_array[5 * x][
                    5 * y + 4] \
                    = image_array[5 * x + 1][5 * y + 4] = image_array[5 * x + 2][5 * y + 4] = \
                    image_array[5 * x + 3][5 * y + 4] = image_array[5 * x + 4][5 * y + 4] = color
        img = Image.fromarray(image_array)
        img.save(filename)

    def generate_map_image_with_player(self, x, y, name):
        map_copy = self.map_list.copy()
        map_copy[x][y] = 6
        image_array = np.zeros((self.size * 5, self.size * 5, 3), dtype=np.uint8)
        for x in range(self.size):
            for y in range(self.size):
                if map_copy[x][y] == 0:
                    color = [27, 122, 49]
                elif map_copy[x][y] == 1:
                    color = [45, 220, 86]
                elif map_copy[x][y] == 2:
                    color = [45, 180, 220]
                elif map_copy[x][y] == 3:
                    color = [176, 176, 176]
                elif map_copy[x][y] == 4:
                    color = [44, 115, 220]
                else:
                    color = [255, 0, 0]
                image_array[5 * x][5 * y] = image_array[5 * x + 1][5 * y] = image_array[5 * x + 2][5 * y] = \
                    image_array[5 * x + 3][5 * y] = image_array[5 * x + 4][5 * y] = image_array[5 * x][5 * y + 1] \
                    = image_array[5 * x + 1][5 * y + 1] = image_array[5 * x + 2][5 * y + 1] = \
                    image_array[5 * x + 3][5 * y + 1] = image_array[5 * x + 4][5 * y + 1] = image_array[5 * x][
                    5 * y + 2] \
                    = image_array[5 * x + 1][5 * y + 2] = image_array[5 * x + 2][5 * y + 2] = \
                    image_array[5 * x + 3][5 * y + 2] = image_array[5 * x + 4][5 * y + 2] = image_array[5 * x][
                    5 * y + 3] \
                    = image_array[5 * x + 1][5 * y + 3] = image_array[5 * x + 2][5 * y + 3] = \
                    image_array[5 * x + 3][5 * y + 3] = image_array[5 * x + 4][5 * y + 3] = image_array[5 * x][
                    5 * y + 4] \
                    = image_array[5 * x + 1][5 * y + 4] = image_array[5 * x + 2][5 * y + 4] = \
                    image_array[5 * x + 3][5 * y + 4] = image_array[5 * x + 4][5 * y + 4] = color
        img = Image.fromarray(image_array)
        img.save(name)


if __name__ == "__main__":
    map_size = input('What map size do you want? ')
    map_size = int(map_size)
    my_map = Map(map_size)
    my_map.generate_map_image('test.png')
