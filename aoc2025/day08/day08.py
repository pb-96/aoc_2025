from data_loader import DayType
from typing import List
from dataclasses import dataclass


@dataclass(order=True)
class Coord:
    x: int
    y: int
    z: int

    def squared_distance_to(self, other: "Coord") -> int:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2


class UnionFind:
    def __init__(self):
        self.sets: list[set[int]] = []

    def find_set_index(self, item: int) -> int:
        for idx, s in enumerate(self.sets):
            if item in s:
                return idx
        return -1

    def union(self, i: int, j: int) -> None:
        idx_i = self.find_set_index(i)
        idx_j = self.find_set_index(j)

        match (idx_i > -1, idx_j > -1):
            case (False, False):
                self.sets.append({i, j})
            case (True, False):
                self.sets[idx_i].add(j)
            case (False, True):
                self.sets[idx_j].add(i)
            case (True, True) if idx_i != idx_j:
                self.sets[idx_i] |= self.sets[idx_j]
                del self.sets[idx_j]

    @property
    def num_sets(self) -> int:
        return len(self.sets)

    def get_sorted_sizes(self, reverse: bool = True) -> list[int]:
        return sorted([len(s) for s in self.sets], reverse=reverse)


def parse_coords(data: List[str]) -> List[Coord]:
    return [Coord(*map(int, line.split(","))) for line in data]


def compute_pairwise_distances(coords: List[Coord]) -> list[tuple[tuple[int, int], int]]:
    pairs = {}
    for i, coord1 in enumerate(coords):
        for j, coord2 in enumerate(coords[i + 1:], i + 1):
            pairs[(i, j)] = coord1.squared_distance_to(coord2)
    return sorted(pairs.items(), key=lambda x: x[1])


class DayEight(DayType):
    day_name: str = "day08"

    def part_one(self, data: List[str]):
        coords = parse_coords(data)
        sorted_pairs = compute_pairwise_distances(coords)

        uf = UnionFind()
        for (i, j), _ in sorted_pairs[:1000]:
            uf.union(i, j)

        sizes = uf.get_sorted_sizes()
        return sizes[0] * sizes[1] * sizes[2]

    def part_two(self, data: List[str]):
        coords = parse_coords(data)
        sorted_pairs = compute_pairwise_distances(coords)

        uf = UnionFind()
        connected = set()

        for (i, j), _ in sorted_pairs:
            connected.add(i)
            connected.add(j)
            uf.union(i, j)

            if len(connected) == len(coords) and uf.num_sets == 1:
                return coords[i].x * coords[j].x
