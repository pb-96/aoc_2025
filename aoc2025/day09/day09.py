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
        rectangles = [
            (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            for (x1, y1), (x2, y2) in combinations(raw_coords, 2)
        ]
        areas = [(x2 - x1 + 1) * (y2 - y1 + 1) for (x1, y1, x2, y2) in rectangles]
        return max(compress(areas, map(poly.contains, starmap(box, rectangles))))