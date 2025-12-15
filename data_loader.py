from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Set, Callable, ClassVar
from functools import partial
from datetime import datetime
import requests

BASE_URL_TEMPLATE: str = "https://adventofcode.com/{year}/day/{day}/input"


@dataclass
class DayType:
    day_name: str
    instances: ClassVar[List["DayType"]] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Register the class itself, not instances
        DayType.instances.append(cls)

    def get_name(self):
        return self.day_name

    def part_one(self):
        raise NotImplementedError("Not Implemented")

    def part_two(self):
        raise NotImplementedError("Not Implemented")

    def both_parts(self, data: List[str]) -> Tuple[int, int]:
        print(f"day => {self.day_name}")
        value = self.part_one(data)
        print(f"Part One => {value}")
        part_two = self.part_two(data)
        print(f"Part Two => {part_two}")
        print("*" * 100)
        return value, part_two

    def __repr__(self):
        return f"DayType(day_name={self.day_name})"


def find_data_file(location: Path, day_name: str) -> List[str]:
    all_files = [
        f for f in location.iterdir() if f.name.endswith(".txt") and f.stem == day_name
    ]
    assert len(all_files) > 0, "Could not find data file"
    file_path = next(iter(all_files), None)
    assert file_path
    return file_path.read_text().splitlines()


class DisplayNode:
    def __init__(self, curr: Path, children: List["DisplayNode"] = []):
        self.curr = curr
        self.children = children

    def has_children(self):
        return len(self.children) > 0

    def __repr__(self):
        return f"Root={self.curr}, children={self.children}"


def build_display_node(root: Path, predicate: Callable[[Path], bool]):
    given_root = DisplayNode(root, children=[])

    if not root.is_dir():
        return given_root

    for child in root.iterdir():
        if child.is_file() and predicate(given_path=child):
            given_root.children.append(DisplayNode(curr=child))
        elif child.is_dir() and predicate(given_path=child):
            given_root.children.append(build_display_node(child, predicate))
    return given_root


def parse_gitignore_file(gitignore_fp: Path) -> Tuple[Set, Set]:
    txt = gitignore_fp.read_text().splitlines()
    skip_dirs = set()
    skip_files = set()

    for t in txt:
        if not t:
            continue
        elif t.startswith("#"):
            continue
        elif t.startswith("/") or t.endswith("/"):
            skip_dirs.add(t.replace("/", ""))
        else:
            skip_files.add(t)
    return skip_dirs, skip_files


def predicate_path(
    given_path: Path, skip_on_dirs: Set[str], skip_on_files: Set[str]
) -> bool:
    if (
        given_path.is_dir()
        and not given_path.name.startswith(".")
        and given_path.name not in skip_on_dirs
    ):
        return True
    if given_path.is_file() and given_path.suffix not in skip_on_files:
        return True
    return False


def build_and_display_nodes(root, skip_on_dirs, skip_on_files):
    "Utils wrapper to display files and data - helps with Readme's and passing context to an LLM -> this tech exists but wanted to write myself"
    predicate = partial(
        predicate_path, skip_on_dirs=skip_on_dirs, skip_on_files=skip_on_files
    )
    as_display_node = build_display_node(root, predicate)
    display_dir(as_display_node, skip_on_dirs, skip_on_files)


def display_dir(
    as_display_node: DisplayNode,
    skip_on_dirs: Set[str],
    skip_on_files: Set[str],
    tab: str = "\t",
):
    if as_display_node.curr.is_dir():
        print(f"{tab}{as_display_node.curr.name} ---->")
    else:
        print(f"{tab}{as_display_node.curr.name}")

    for child in as_display_node.children:
        if child.has_children():
            print(f"{tab}-{child.curr.name}/ ---->")
            tab_copy = tab * 2
            for inner_child in child.children:
                display_dir(inner_child, skip_on_dirs, skip_on_files, tab_copy)
        else:
            print(f"{tab}{child.curr.name}")


def scrape_input_data(current_time: datetime, dest_path: Path) -> bool:
    day, year = current_time.day, current_time.year
    full_string = BASE_URL_TEMPLATE.format(year=year, day=day)
    try:
        response = requests.get(full_string)
        response.raise_for_status()
        raw_data = response.text.splitlines()
        dest_path.write_text("\n".join(raw_data))
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error scraping input data: {e}")
        return False
