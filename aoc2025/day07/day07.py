from data_loader import DayType
from collections import defaultdict
from copy import deepcopy


class DaySeven(DayType):
    day_name: str = "day07"

    def display_grid(self, grid: List[List[str]]) -> None:
        for row in grid:
            print("".join(row))

    def draw_line(self, draw_copy, x: int, y: int) -> None:
        draw_copy[y][x - 1] = "|"
        draw_copy[y][x + 1] = "|"

    def parse_data(self, data):
        _map = []
        st = None
        for y, line in enumerate(data):
            row = list(line)
            if y == 0 and st is None:
                for x, c in enumerate(row):
                    if c == "S":
                        st = (y, x)
            _map.append(row)
        return _map, st

    def part_one(self, data):
        _map, (y, x) = self.parse_data(data)
        drawn_copy = deepcopy(data)

        beams = {x}
        splitters = 0

        while True:
            if y > len(_map) - 2:
                break

            y += 1
            next_beams = set()
            beams = next_beams
        return splitters

    def part_two(self, data):
        _map, (y, x) = self.parse_data(data)

        beams = defaultdict(int)
        beams[x] = 1

        while True:
            if y > len(_map) - 2:
                break

            y += 1
            next_beams = defaultdict(int)

            for x in beams:
                n = beams[x]
                if _map[y][x] == "^":
                    next_beams[x - 1] += n
                    next_beams[x + 1] += n
                else:
                    next_beams[x] += n
            beams = next_beams

        return sum(beams.values())
