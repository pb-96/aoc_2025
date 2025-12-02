from day01.day01 import DayOne
from day02.day02 import DayTwo
from data_loader import find_data_file, DayType
from typing import List
from pathlib import Path

ROOT = Path(".")

ALL_ENTRIES: List[DayType] = [
    DayOne,
    DayTwo
]

if __name__ == "__main__":
    for entry in ALL_ENTRIES:
        instance: DayType = entry()
        day_name = ROOT / instance.get_name()
        data = find_data_file(day_name)
        part_one, part_two = instance.both_parts(data)

        print("*" * 100)
        print(f"Answer for Day => {instance.day_name}")
        print(f"Part One Answer => {part_two}")
        print(f"Part Two Answer => {part_two}")
        print("*" * 100)

