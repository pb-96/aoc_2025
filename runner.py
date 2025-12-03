from day01.day01 import DayOne
from day02.day02 import DayTwo
from day03.day03 import DayThree
from data_loader import find_data_file, DayType
from typing import List
from pathlib import Path

ROOT = Path().cwd()
gitignore_file = ROOT / ".gitignore"

ALL_ENTRIES: List[DayType] = [
    DayOne,
    DayTwo,
    DayThree
]

if __name__ == "__main__":
    for entry in ALL_ENTRIES:
        instance: DayType = entry()
        location = ROOT / instance.get_name()
        data = find_data_file(location, instance.get_name())
        instance.both_parts(data)
