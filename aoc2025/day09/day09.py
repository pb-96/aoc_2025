from data_loader import DayType
from typing import List
from dataclasses import dataclass
from itertools import combinations, starmap, compress
from shapely import Polygon, box


@dataclass
class Point:
    x: int
    y: int

    def area_to(self, other: "Point") -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


@dataclass
class GraphPoint:
    point: Point
    edges: List[Point]


class DayNine(DayType):
    day_name: str = "day09"
    corner_delim = "#"

    def create_points(self, data: List[str]) -> List[Point]:
        points = [Point(int(x), int(y)) for x, y in map(lambda x: x.split(","), data)]
        return points

    def part_one(self, data: List[str]):
        points = self.create_points(data)
        max_area = 0

        for point in points:
            for point_j in points:
                if point == point_j:
                    continue
                area = point.area_to(point_j)
                max_area = max(max_area, area)
        return max_area

    def part_two(self, data: List[str]):
        points = self.create_points(data)
        raw_coords = [(point.x, point.y) for point in points]
        poly = Polygon(raw_coords)
        candidates = sorted(
            (
                (
                    p1.area_to(p2),
                    min(p1.x, p2.x),
                    min(p1.y, p2.y),
                    max(p1.x, p2.x),
                    max(p1.y, p2.y),
                )
                for p1, p2 in combinations(points, 2)
            ),
            reverse=True,
        )

        for area, *bounds in candidates:
            if poly.contains(box(*bounds)):
                return area
        return 0
