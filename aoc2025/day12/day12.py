from typing import Dict, List, Tuple
from data_loader import DayType

FILL_RATIO_THRESHOLD = 1.3


def split_into_sections(data: List[str]) -> List[List[str]]:
    sections = []
    current = []
    for line in data:
        if line == "":
            if current:
                sections.append(current)
                current = []
        else:
            current.append(line)
    if current:
        sections.append(current)
    return sections


def parse_present(lines: List[str]) -> Tuple[int, int]:
    present_id = int(lines[0].rstrip(":"))
    grid = lines[1:]
    size = sum(row.count("#") for row in grid)
    return present_id, size


def parse_presents(sections: List[List[str]]) -> Dict[int, int]:
    sizes = {}
    for section in sections:
        if ":" in section[0] and "x" not in section[0]:
            present_id, size = parse_present(section)
            sizes[present_id] = size
    return sizes


def parse_region(line: str) -> Tuple[int, List[int]]:
    dimensions, counts = line.split(": ")
    rows, cols = map(int, dimensions.split("x"))
    grid_size = rows * cols
    present_counts = list(map(int, counts.split()))
    return grid_size, present_counts


def calculate_total_present_size(
    present_counts: List[int], sizes: Dict[int, int]
) -> int:
    return sum(count * sizes[i] for i, count in enumerate(present_counts))


class DayTwelve(DayType):
    day_name: str = "day12"

    def part_one(self, data: List[str]) -> int:
        sections = split_into_sections(data)
        present_sections = sections[:-1]
        region_lines = sections[-1]

        sizes = parse_presents(present_sections)
        easy_count = 0

        for line in region_lines:
            grid_size, present_counts = parse_region(line)
            total_present_size = calculate_total_present_size(present_counts, sizes)

            if total_present_size * FILL_RATIO_THRESHOLD < grid_size:
                easy_count += 1

        return easy_count

    def part_two(self, data: List[str]) -> int:
        return 0
