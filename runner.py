from day01.day01 import DayOne
from day02.day02 import DayTwo
from day03.day03 import DayThree
from data_loader import find_data_file, DayType, parse_gitignore_file, build_and_display_nodes
from typing import List
from pathlib import Path

ROOT = Path().cwd()
gitignore_file = ROOT / ".gitignore"

ALL_ENTRIES: List[DayType] = [DayOne, DayTwo, DayThree]


# TODO: Make a cli tool and make this configurable to run
def init_display_dir():
    gitignore_path = ROOT / ".gitignore"
    if not gitignore_path.exists():
        return

    skip_dirs, skip_files = parse_gitignore_file(gitignore_path)
    build_and_display_nodes(ROOT, skip_dirs, skip_files)


if __name__ == "__main__":
    init_display_dir()
    for entry in ALL_ENTRIES:
        instance: DayType = entry()
        location = ROOT / instance.get_name()
        data = find_data_file(location, instance.get_name())
        instance.both_parts(data)
