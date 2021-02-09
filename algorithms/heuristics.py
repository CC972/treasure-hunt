from enum import Enum
from math import sqrt

from model.game import Location


def euclidean(loc_1: Location, loc_2: Location):
    return sqrt((loc_1.x - loc_2.x) ** 2 + (loc_1.y - loc_2.y) ** 2)


def manhattan(loc_1: Location, loc_2: Location):
    return abs(loc_1.x - loc_2.x) + abs(loc_1.y - loc_2.y)


class Distance(Enum):

    EUCLIDEAN = euclidean,
    MANHATTAN = manhattan,

    def __call__(self, loc_1: Location, loc_2: Location):
        return self.value[0](loc_1, loc_2)
