from data_loader import (
    find_data_file,
    DayType,
    parse_gitignore_file,
    build_and_display_nodes,
)
from pathlib import Path
from datetime import datetime

# TODO Make this import dynamic based of the year which is passed in from the user
from aoc2025 import *

ROOT = Path().cwd()
gitignore_file = ROOT / ".gitignore"


# TODO: Make a cli tool and make this configurable to run
def init_display_dir():
    gitignore_path = ROOT / ".gitignore"
    if not gitignore_path.exists():
        return

    skip_dirs, skip_files = parse_gitignore_file(gitignore_path)
    build_and_display_nodes(ROOT, skip_dirs, skip_files)


if __name__ == "__main__":
    init_display_dir()

    # SO OVER ENGINEERED LOL
    current_time = datetime.now()
    current_year = current_time.year

    for raw_cls in DayType.instances:
        day: DayType = raw_cls(raw_cls.get_name(raw_cls))
        # TODO Make this import dynamic based of the year which is passed in from the user
        location = ROOT / f"aoc{current_year}" / day.get_name()
        data = find_data_file(location, day.get_name())
        day.both_parts(data)
