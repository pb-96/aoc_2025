from data_loader import (
    find_data_file,
    DayType,
    parse_gitignore_file,
    build_and_display_nodes,
)
from pathlib import Path
from datetime import datetime

import importlib
from typer import Typer

app = Typer()


current_time = datetime.now()
current_year = current_time.year
string_package_name = f"aoc{current_year}"

importlib.import_module(string_package_name)

ROOT = Path().cwd()
gitignore_file = ROOT / ".gitignore"


# TODO: Make a cli tool and make this configurable to run
def init_display_dir():
    gitignore_path = ROOT / ".gitignore"
    if not gitignore_path.exists():
        return

    skip_dirs, skip_files = parse_gitignore_file(gitignore_path)
    build_and_display_nodes(ROOT, skip_dirs, skip_files)


@app.command()
def main(given_current_year: int | None = None):
    given_current_year = given_current_year or current_year
    init_display_dir()
    for raw_cls in DayType.instances:
        day: DayType = raw_cls(raw_cls.get_name(raw_cls))
        location = ROOT / f"aoc{given_current_year}" / day.get_name()
        data = find_data_file(location, day.get_name())
        day.both_parts(data)


if __name__ == "__main__":
    app()
