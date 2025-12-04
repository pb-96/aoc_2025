from data_loader import DayType
from typing import List, Tuple

DIRECTIONS = [
    (1, 1),
    (-1, 1),
    (1, -1),
    (-1, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
    (0, -1),
]


class DayFour(DayType):
    day_name = "day04"

    def normalize_grid(self, data: List[str]) -> List[List[str]]:
        grid = [list(string) for  string in data]
        return grid

    def bfs(self, pos: Tuple[int, int], grid: List[List[str]]) -> int:
        row, col = pos
        total_found = 0

        for direction in DIRECTIONS:
            l, r = direction[0] + row, direction[1] + col
            if l < 0 or l >= len(grid):
                continue
            if r < 0 or r >= len(grid[0]):
                continue

            char_match = grid[l][r] == "@"
            total_found += char_match

        return 1 if total_found < 4 else 0

    def part_one(self, data):
        as_matrix = self.normalize_grid(data)
        count = 0
        for r_idx, row in enumerate(as_matrix):
            for c_idx, col in enumerate(row):
                if col == "@":
                    count += self.bfs((r_idx, c_idx), as_matrix)
        return count

    def part_two(self, data: List[str]):
        as_matrix = self.normalize_grid(data)
        total_count = 0

        while True:
            to_swop = []
            for r_idx, row in enumerate(as_matrix):
                for c_idx, col in enumerate(row):
                    if col == "@":
                        count = self.bfs((r_idx, c_idx), as_matrix)
                        if count:
                            to_swop.append((r_idx, c_idx))
            
            total_count += len(to_swop)
            for l, r in to_swop:
                as_matrix[l][r] = "x"

            if not len(to_swop):
                break

        return total_count
