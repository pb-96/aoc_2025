from data_loader import (
    find_data_file,
    DayType,
    parse_gitignore_file,
    build_and_display_nodes,
    scrape_input_data,
)
from pathlib import Path
from datetime import datetime
from generate_boiler_plate import (
    generate_boiler_plate_string,
    generate_init_file_string,
)
import importlib
from typer import Typer

app = Typer()


current_time = datetime.now()
current_year = current_time.year
string_package_name = f"aoc{current_year}"

importlib.import_module(string_package_name)

ROOT = Path().cwd()
gitignore_file = ROOT / ".gitignore"


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


@app.command()
def init_day():
    day_string = f"day{current_time.day:02d}"
    new = ROOT / f"aoc{current_year}" / day_string
    if new.exists():
        print(f"Day {day_string} already exists")
        return
    new.mkdir(parents=True, exist_ok=True)
    py_file = new / f"{day_string}.py"
    py_file.touch()
    txt_file = new / f"{day_string}.txt"
    txt_file.touch()
    py_file.write_text(generate_boiler_plate_string(current_time))
    (ROOT / f"aoc{current_year}" / "__init__.py").write_text(
        generate_init_file_string(current_time)
    )
    scrape_input_data(current_time, txt_file)


if __name__ == "__main__":
    app()
