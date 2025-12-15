from data_loader import DayType
from typing import List, Tuple
from collections import defaultdict


class DaySeven(DayType):
    day_name: str = "day07"

    def display_grid(self, grid: List[List[str]]) -> None:
        for row in grid:
            print("".join(row))

    def draw_line(
        self, draw_copy, y: int, x: int
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        draw_copy[y][x - 1] = "|"
        draw_copy[y][x + 1] = "|"
        return (y, x - 1), (y, x + 1)

    def parse_data(self, data):
        _map = []
        for line in data:
            _map.append(list(line))
        return _map

    def locate_start(self, _map):
        for y, row in enumerate(_map):
            for x, cell in enumerate(row):
                if cell == "S":
                    return y, x
        return None

    def part_one(self, data):
        st = self.locate_start(data)
        assert st is not None, "Start not found"
        y,x = st
        _map = self.parse_data(data)
        beams = {x}
        splitters = 0

        while True:
            if y > len(_map) - 2:
                break

            y += 1
            next_beams = set()

            for x in beams:
                if _map[y][x] == "^":
                    next_beams.add(x - 1)
                    next_beams.add(x + 1)
                    splitters += 1
                else:
                    next_beams.add(x)
            beams = next_beams
        return splitters

    def part_two(self, data):
        st = self.locate_start(data)
        assert st is not None, "Start not found"
        y,x = st
        _map = self.parse_data(data)

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
