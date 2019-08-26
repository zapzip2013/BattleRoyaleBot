# Code written by Alexander Holmstock

from enum import Enum


class Items(Enum):
    SWORD = 1
    BOW_AND_ARROW = 2
    MAGIC_WAND = 3
    DAGGER = 4
    CAT = 5
    RUNNING_SHOES = 6
    NONE = 7


class Directions(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


class Actions(Enum):
    MOVE = 1
    EQUIP = 2
    SEARCH = 3
    TRACK = 4
    USE = 5


class Player(object):

    default_actions = 3
    move_distance = 3

    def __init__(self, x, y, name, map_size):
        self.x = x
        self.y = y
        self.name = name
        self.equipped = Items.NONE
        self.items = []
        self.bonus_actions = 0
        self.actions = Player.default_actions
        self.action_list = []
        self.alive = True
        self.map_size = map_size

    # check to see if the player has the item(of type Items(Enum)) passed, if they do, equip and true, else false
    def equip(self, item):
        enum_item = self.convert_string_to_enum(item)
        if enum_item in self.items:
            if self.equipped == Items.RUNNING_SHOES:
                self.bonus_actions -= 1
            self.equipped = enum_item
            if self.equipped == Items.RUNNING_SHOES:
                self.bonus_actions += 1
            return True
        else:
            return False

    def has_actions(self):
        if self.actions == 0:
            return False
        else:
            return True

    def kill(self):
        self.alive = False

    def add_action(self, action):
        self.action_list.append(action)

    def reset_actions(self):
        self.actions = Player.default_actions + self.bonus_actions

    def move(self, direction):
        if direction.upper() == "NORTH":
            if self.y - self.move_distance >= 0:
                self.y -= self.move_distance
                return True
            else:
                return False
        if direction.upper() == "EAST":
            if self.x + self.move_distance <= self.map_size-1:
                self.x += self.move_distance
                return True
            else:
                return False
        if direction.upper() == "SOUTH":
            if self.y + self.move_distance <= self.map_size-1:
                self.y += self.move_distance
                return True
            else:
                return False
        if direction.upper() == "WEST":
            if self.x - self.move_distance >= 0:
                self.x -= self.move_distance
                return True
            else:
                return False
        else:
            return False

    def find_item(self, item):
        if item.upper() == "SWORD":
            self.items.append(Items.SWORD)
        if item.upper() == "BOW_AND_ARROW":
            self.items.append(Items.BOW_AND_ARROW)
        if item.upper() == "MAGIC_WAND":
            self.items.append(Items.MAGIC_WAND)
        if item.upper() == "DAGGER":
            self.items.append(Items.DAGGER)
        if item.upper() == "CAT":
            self.items.append(Items.CAT)
        if item.upper() == "RUNNING_SHOES":
            self.items.append(Items.RUNNING_SHOES)

    def convert_string_to_enum(self, the_str):
        if the_str.upper() == "SWORD":
            return Items.SWORD
        if the_str.upper() == "BOW_AND_ARROW":
            return Items.BOW_AND_ARROW
        if the_str.upper() == "MAGIC_WAND":
            return Items.MAGIC_WAND
        if the_str.upper() == "DAGGER":
            return Items.DAGGER
        if the_str.upper() == "CAT":
            return Items.CAT
        if the_str.upper() == "RUNNING_SHOES":
            return Items.RUNNING_SHOES
        return Items.NONE

    # GETTERS
    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_equipped(self):
        return self.equipped

    def get_items(self):
        return self.items

    def get_actions(self):
        return self.actions


if __name__ == "__main__":
    print("Testing player.py")
