from typing import List, Tuple
from enum import Enum
from data_loader import DayType
from operator import add, sub
from dataclasses import dataclass

UPPER_LIM = 100
LOWER_LIM = 0


class Direction(Enum):
    L: str = "L"
    R: str = "R"


OPERATOR_MAP = {Direction.L: sub, Direction.R: add}
VALUE_DIR = {
    Direction.L: -1,
    Direction.R: 1,
}

@dataclass
class DayOne(DayType):
    day_name: str = "day01"

    def normalize_row(self, row: int):
        return row if row <= UPPER_LIM else row % UPPER_LIM

    def parse_row(self, row: str):
        return Direction(row[0]), int(row[1:])

    def part_one(self, data: List[str], start_point=50):
        counter = 0
        for row in data:
            direction, rotate = self.parse_row(row)
            rotate = self.normalize_row(rotate)
            opp = OPERATOR_MAP.get(direction)
            temp = opp(start_point, rotate)

            if temp < LOWER_LIM:
                temp = UPPER_LIM - abs(temp)
            elif temp == LOWER_LIM:
                counter += 1
                temp = UPPER_LIM - temp
            elif temp >= UPPER_LIM:
                temp = temp - UPPER_LIM

            if temp == 0:
                counter += 1

            start_point = temp

        return counter

    def part_two(self, data, start_point=50):
        counter = 0
        for row in data:
            direction, r = self.parse_row(row)
            skips, rotate = divmod(r, 100)
            counter += skips
            if direction == Direction.R:
                if start_point + rotate >= 100:
                    counter += 1
            else:
                if start_point > 0 and (start_point - rotate) <= 0:
                    counter += 1
            start_point = (start_point + rotate * VALUE_DIR.get(direction)) % 100

        return counter
